# Copyright 2014 Bevbot LLC, All Rights Reserved
#
# This file is part of the Pykeg package of the Kegbot project.
# For more information on Pykeg or Kegbot, see http://kegbot.org/
#
# Pykeg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pykeg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pykeg.  If not, see <http://www.gnu.org/licenses/>.

"""High-level interface to Django backend."""

from __future__ import absolute_import

import datetime
import logging

from django.db import transaction
from django.utils import timezone
from django.db.utils import IntegrityError
from pykeg import notification
from pykeg.core import defaults
from pykeg.core import keg_sizes
from pykeg.core.util import SuppressTaskErrors
from pykeg.core.cache import KegbotCache
from pykeg.web.auth import get_auth_backend
from pykeg.web.auth import AuthException
from pykeg.web.auth import UserExistsException
from pykeg.util.email import build_message

from pykeg.core import kb_common
from pykeg.core import models
from pykeg.core import stats
from pykeg.core import time_series

from pykeg.backend.exceptions import *
from pykeg.web import tasks

class KegbotBackend(object):
    """Provides high-level operations against the Kegbot system."""

    def __init__(self):
        self._logger = logging.getLogger('backend')
        self.cache = KegbotCache()

    @transaction.atomic
    def create_new_user(self, username, email, password=None, photo=None):
        """Creates and returns a User for the given username."""
        try:
            user = get_auth_backend().register(username=username, email=email,
                    password=password, photo=photo)
            return user
        except UserExistsException as e:
            raise UserExistsError(e)
        except AuthException as e:
            raise BackendError(e)

    @transaction.atomic
    def create_tap(self, name, meter_name, toggle_name=None, ticks_per_ml=None):
        """Creates and returns a new KegTap.

        Args:
          name: The human-meaningful name for the tap, for instance, "Main Tap".
          meter_name: The unique sensor name for the tap, for instance,
              "kegboard.flow0".
          toggle_name: If the tap is connected to a relay, this specifies its
              name, for instance, "kegboard.relay0".
          ticks_per_ml: The number of flow meter ticks per milliliter of fluid
              on this tap's meter.

        Returns:
            The new KegTap instance.
        """
        tap = models.KegTap.objects.create(name=name)
        tap.save()

        meter = models.FlowMeter.get_or_create_from_meter_name(meter_name)
        meter.tap = tap
        if ticks_per_ml:
            meter.ticks_per_ml = ticks_per_ml
        meter.save()

        if toggle_name:
            toggle = models.FlowToggle.get_or_create_from_toggle_name(toggle_name)
        return tap

    @transaction.atomic
    def create_auth_token(self, auth_device, token_value, username=None):
        """Creates a new AuthenticationToken.

        The combination of (auth_device, token_value) must be unique within the
        system.

        Args:
            auth_device: The name of the authentication device, for instance,
                "core.rfid".
            token_value: The opaque string value of the token, which is typically
                unique within the `auth_device` namespace.
            username: The User with which to associate this Token.

        Returns:
            The newly-created AuthenticationToken.
        """
        token = models.AuthenticationToken.objects.create(
            auth_device=auth_device, token_value=token_value)
        if username:
            user = get_user(username)
            token.user = user
        token.save()
        return token

    def record_drink(self, tap, ticks, volume_ml=None, username=None,
        pour_time=None, duration=0, shout='', tick_time_series='', photo=None,
        do_postprocess=True, spilled=False):
        """Records a new drink against a given tap.

        The tap must have a Keg assigned to it (KegTap.current_keg), and the keg
        must be active.

        Args:
            tap: A KegTap or matching meter name.
            ticks: The number of ticks observed by the flow sensor for this drink.
            volume_ml: The volume, in milliliters, of the pour.  If specifed, this
                value is saved as the Drink's actual value.  If not specified, a
                volume is computed based on `ticks` and the meter's
                `ticks_per_ml` setting.
            username: The username with which to associate this Drink, or None for
                an anonymous Drink.
            pour_time: The datetime of the drink.  If not supplied, the current
                date and time will be used.
            duration: Number of seconds it took to pour this Drink.  This is
                optional information not critical to the record.
            shout: A short comment left by the user about this Drink.  Optional.
            tick_time_series: Vector of flow update data, used for diagnostic
                purposes.
            do_postprocess: Set to False during bulk inserts.
            spilled: If drink is recorded as spill, the volume is added to spilled_ml
                and the "drink" is not saved as an event.

        Returns:
            The newly-created Drink instance.
        """

        with transaction.atomic():
            tap = self._get_tap(tap)
            if not tap.is_active or not tap.current_keg:
                raise BackendError("No active keg at this tap")

            keg = tap.current_keg

            if spilled:
                keg.spilled_ml += volume_ml
                keg.save(update_fields=['spilled_ml'])
                return None

            if volume_ml is None:
                meter = tap.current_meter()
                if not meter:
                    raise BackendError("Tap has no meter, can't compute volume")
                volume_ml = float(ticks) / meter.ticks_per_ml

            user = None
            if username:
                user = get_user(username)
            else:
                user = models.KegbotSite.get().default_user
                if not user:
                    user = models.User.objects.get(username='guest')

            if not pour_time:
                pour_time = timezone.now()

            if tick_time_series:
                try:
                    # Validate the time series by parsing it; canonicalize it by generating
                    # it again.  If malformed, just junk it; it's non-essential information.
                    tick_time_series = time_series.to_string(time_series.from_string(tick_time_series))
                except ValueError, e:
                    self._logger.warning('Time series invalid, ignoring. Error was: %s' % e)
                    tick_time_series = ''

            d = models.Drink(ticks=ticks, keg=keg, user=user,
                volume_ml=volume_ml, time=pour_time, duration=duration,
                shout=shout, tick_time_series=tick_time_series)
            models.DrinkingSession.AssignSessionForDrink(d)
            d.save()

            keg.served_volume_ml += volume_ml
            keg.save(update_fields=['served_volume_ml'])

        self.cache.update_generation()

        if photo:
            with transaction.atomic():
                pic = models.Picture.objects.create(
                    image=photo,
                    user=d.user,
                    keg=d.keg,
                    session=d.session
                )
                d.picture = pic
                d.save()

        if do_postprocess:
            self.build_stats(d.id)
            with transaction.atomic():
                events = models.SystemEvent.build_events_for_drink(d)
                tasks.schedule_tasks(events)

        return d

    def cancel_drink(self, drink, spilled=False):
        """Permanently deletes a Drink from the system.

        Associated data, such as SystemEvent, Pictures, and other data, will
        be destroyed along with the drink. Statistics and session data will be
        recomputed after the drink is destroyed.

        Args:
            drink_id: The Drink, or id of the Drink, to cancel.
            spilled: If True, after canceling the Drink, the drink's volume will
                be added to its Keg's "spilled" total.  This is is typically useful
                for removing test pours from the system while still accounting for
                the lost volume.

        Returns:
            The deleted drink.
        """
        with transaction.atomic():
            if not isinstance(drink, models.Drink):
                drink = models.Drink.objects.get(id=drink)

            session = drink.session
            drink_id = drink.id
            keg = drink.keg
            volume_ml = drink.volume_ml

            keg_update_fields = ['served_volume_ml']
            keg.served_volume_ml -= volume_ml

            # Transfer volume to spillage if requested.
            if spilled and volume_ml and drink.keg:
                keg.spilled_ml += volume_ml
                keg_update_fields.append('spilled_ml')

            keg.save(update_fields=keg_update_fields)

            # Delete the drink, including any objects related to it.
            drink.delete()
            session.Rebuild()

        self.build_stats(drink_id)
        self.cache.update_generation()

        return drink

    @transaction.atomic
    def assign_drink(self, drink, user):
        """Assigns, or re-assigns, a previously-recorded Drink.

        Statistics and session data will be recomputed as a side-effect
        of any change to user assignment.  (If the drink is already assigned
        to the given user, this method is a no-op).

        Args:
            drink: The Drink object (or drink id) to assign.
            user: The User object (or username) to set as the owner,
                or None for anonymous.

        Returns:
            The drink.
        """
        with transaction.atomic():
            drink = get_drink(drink)
            user = get_user(user)
            if drink.user == user:
                return drink

            drink.user = user
            drink.save()

            for e in drink.events.all():
                e.user = user
                e.save()
            if drink.picture:
                drink.picture.user = user
                drink.picture.save()

            drink.session.Rebuild()

        self.build_stats(drink.id)
        self.cache.update_generation()

        return drink

    def set_drink_volume(self, drink, volume_ml):
        """Updates the drink volume."""
        if volume_ml == drink.volume_ml:
            return

        with transaction.atomic():
            difference = volume_ml - drink.volume_ml
            drink.volume_ml = volume_ml
            drink.save(update_fields=['volume_ml'])

            keg = drink.keg
            keg.served_volume_ml += difference
            keg.save(update_fields=['served_volume_ml'])

            drink.session.Rebuild()

        self.build_stats(drink.id)
        self.cache.update_generation()

    @transaction.atomic
    def log_sensor_reading(self, sensor_name, temperature, when=None):
        """Logs a ThermoSensor reading.

        To avoid an excessive number of entries, the system limits temperature
        readings to one per minute.  If there is already a recording for the
        given time period, that record will be updated with the current temperature
        ("last one wins").

        Regardless of this record's timestamp, any records older than
        `kb_common.THERMO_SENSOR_HISTORY_MINUTES` will be deleted as a side effect
        of this call.

        Args:
            sensor_name: The name of the sensor, corresponding to
                ThermoSensor.raw_name.
            temperature: Temperature, in celsius degrees.  Values outside of the
                range specified in `kb_common.THERMO_SENSOR_RANGE` will be
                rejected.
            when: If specified, a datetime of the recording, otherwise the current
                time is used.

        Returns:
            The record for this reading.
        """
        now = timezone.now()
        if not when:
            when = now

        # The maximum resolution of ThermoSensor records is 1 minute.  Round the
        # time down to the nearest minute; if a record already exists for this time,
        # replace it.
        when = when.replace(second=0, microsecond=0)

        # If the temperature is out of bounds, reject it.
        min_val = kb_common.THERMO_SENSOR_RANGE[0]
        max_val = kb_common.THERMO_SENSOR_RANGE[1]
        if temperature < min_val or temperature > max_val:
            raise ValueError('Temperature out of bounds')

        sensor = self._get_sensor_from_name(sensor_name)
        log_defaults = {
            'temp': temperature,
        }
        record, created = models.Thermolog.objects.get_or_create(sensor=sensor,
          time=when, defaults=log_defaults)
        record.temp = temperature
        record.save()

        # Delete old entries.
        keep_time = now - datetime.timedelta(
            minutes=kb_common.THERMO_SENSOR_HISTORY_MINUTES)
        old_entries = models.Thermolog.objects.filter(time__lt=keep_time)
        old_entries.delete()

        return record

    @transaction.atomic
    def get_auth_token(self, auth_device, token_value):
        """Fetches the AuthenticationToken matching the given parameters.

        Args:
            auth_device: The requested token's auth_device.
            token_value: The token's value, typically unique within auth_device.

        Returns:
            The matching token.

        Raises:
            NoTokenError: No matching token could be found.
        """
        if token_value and auth_device in kb_common.AUTH_MODULE_NAMES_HEX_VALUES:
            token_value = token_value.lower()
        try:
            return models.AuthenticationToken.objects.get(auth_device=auth_device,
                token_value=token_value)
        except models.AuthenticationToken.DoesNotExist:
            # TODO(mikey): return None instead of raising.
            raise NoTokenError

    def start_keg(self, tap, beverage=None, keg_type=keg_sizes.HALF_BARREL,
            full_volume_ml=None, beverage_name=None, beverage_type=None,
            producer_name=None, style_name=None, when=None):
        """Activates a new keg at the given tap.

        The tap must be inactive (tap.current_keg == None), otherwise a
        ValueError will be thrown.

        A beverage must be specified, either by providing an existing
        Beverage instance as `beverage`, or by specifying values for
        `beverage_type`, `beverage_name`, `producer_name`,
        and `style_name`.

        When using the latter form, the system will attempt to match
        the string type parameters against an already-existing Beverage.
        Otherwise, a new Beverage will be created.

        Args:
            tap: The KegTap or meter name to tap against.
            beverage: The type of beverage, as a Beverage object.
            keg_type: The type of physical keg, from keg_sizes.
            full_volume_ml: The keg's original unserved volume.  If unspecified,
                will be interpreted from keg_type.  It is an error to omit this
                parameter when keg_type is OTHER.
            beverage_name: The keg's beverage name.  Must be given with
                `producer_name` and `style_name`;
                `beverage` must be None.
            beverage_type: The keg beverage type.
            producer_name: The brewer or producer of this beverage.
            style_name: The style of this beverage.
            when: Keg activation date and time. If not specified, current
                time will be used.

        Returns:
            The new keg instance.
        """
        with transaction.atomic():
            tap = self._get_tap(tap)

            if tap.is_active():
                raise ValueError('Tap is already active, must end keg first.')

            if beverage:
                if beverage_type or beverage_name or producer_name or style_name:
                    raise ValueError(
                        'Cannot give beverage_type, beverage_name, producer_name, or style_name with beverage')
            else:
                if not beverage_type:
                    raise ValueError('Must supply beverage_type when beverage is None')
                if not beverage_name:
                    raise ValueError('Must supply beverage_name when beverage is None')
                if not producer_name:
                    raise ValueError('Must supply producer_name when beverage is None')
                if not style_name:
                    raise ValueError('Must supply style_name when beverage is None')
                producer = models.BeverageProducer.objects.get_or_create(name=producer_name)[0]
                beverage = models.Beverage.objects.get_or_create(name=beverage_name, beverage_type=beverage_type,
                        producer=producer, style=style_name)[0]

            if keg_type not in keg_sizes.DESCRIPTIONS:
                raise ValueError('Unrecognized keg type: %s' % keg_type)
            if full_volume_ml is None:
                full_volume_ml = keg_sizes.VOLUMES_ML[keg_type]

            if not when:
                when = timezone.now()

            keg = models.Keg.objects.create(type=beverage, keg_type=keg_type,
                    online=True, full_volume_ml=full_volume_ml,
                    start_time=when)

        return self.attach_keg(tap, keg)

    def attach_keg(self, tap, keg):
        """Activates a new keg at the given tap (with existing choices).

        The tap must be inactive (tap.current_keg == None), otherwise a
        ValueError will be thrown.

        Since the keg already exists in the database, it is assumed that
        "add_keg" took care of all the error conditions and checking.

        Args:
            tap: The KegTap or meter name to tap against.
            keg_id: The Keg ID to map to tap.

        Returns:
            The new keg instance.
        """
        with transaction.atomic():
            tap = self._get_tap(tap)

            if tap.is_active():
                raise ValueError('Tap is already active, must end keg first.')

            keg.start_time = timezone.now()
            keg.online = True
            keg.save()

            old_keg = tap.current_keg
            if old_keg:
                self.end_keg(tap)

            tap.current_keg = keg
            tap.save()

            events = models.SystemEvent.build_events_for_keg(keg)

        with transaction.atomic():
            tasks.schedule_tasks(events)

        return keg


    def end_keg(self, tap):
        """Takes the current Keg offline at the given tap.

        Args:
            tap: The KegTap object to tap against, or a string matching
                the tap's meter name.

        Returns:
            The old keg.

        Raises:
            ValueError: if the tap is missing or already offline.
        """
        with transaction.atomic():
            tap = self._get_tap(tap)

            if not tap.current_keg:
                raise ValueError('Tap is already offline.')

            keg = tap.current_keg
            keg.online = False
            keg.end_time = timezone.now()
            keg.finished = True
            keg.save()

            tap.current_keg = None
            tap.save()

            events = models.SystemEvent.build_events_for_keg(keg)

        with transaction.atomic():
            tasks.schedule_tasks(events)

        return keg

    @transaction.atomic
    def add_keg(self, beverage=None, keg_type=keg_sizes.HALF_BARREL,
            full_volume_ml=None, beverage_name=None, beverage_type=None,
            producer_name=None, style_name=None, notes=None, description=None):
        """Adds a new keg to the keg room (queue).

        A beverage must be specified, either by providing an existing
        Beverage instance as `beverage`, or by specifying values for
        `beverage_type`, `beverage_name`, `producer_name`,
        and `style_name`.

        When using the latter form, the system will attempt to match
        the string type parameters against an already-existing Beverage.
        Otherwise, a new Beverage will be created.

        Args:
            beverage: The type of beverage, as a Beverage object.
            keg_type: The type of physical keg, from keg_sizes.
            full_volume_ml: The keg's original unserved volume.  If unspecified,
                will be interpreted from keg_type.  It is an error to omit this
                parameter when keg_type is OTHER.
            beverage_name: The keg's beverage name.  Must be given with
                `producer_name` and `style_name`;
                `beverage` must be None.
            beverage_type: The keg beverage type.
            producer_name: The brewer or producer of this beverage.
            style_name: The style of this beverage.
            notes: Notes about this keg.
            description: The keg description (private)

        Returns:
            The new keg instance.
        """
        if beverage:
            if beverage_type or beverage_name or producer_name or style_name:
                raise ValueError(
                    'Cannot give beverage_type, beverage_name, producer_name, or style_name with beverage')
        else:
            if not beverage_type:
                raise ValueError('Must supply beverage_type when beverage is None')
            if not beverage_name:
                raise ValueError('Must supply beverage_name when beverage is None')
            if not producer_name:
                raise ValueError('Must supply producer_name when beverage is None')
            if not style_name:
                raise ValueError('Must supply style_name when beverage is None')
            producer = models.BeverageProducer.objects.get_or_create(name=producer_name)[0]
            beverage = models.Beverage.objects.get_or_create(name=beverage_name, beverage_type=beverage_type,
                    producer=producer, style=style_name)[0]

        if keg_type not in keg_sizes.DESCRIPTIONS:
            raise ValueError('Unrecognized keg type: %s' % keg_type)
        if full_volume_ml is None:
            full_volume_ml = keg_sizes.VOLUMES_ML[keg_type]
        else:
            full_volume_ml = full_volume_ml

        when = timezone.now()

        keg = models.Keg.objects.create(type=beverage, keg_type=keg_type,
                online=False, finished=False, full_volume_ml=full_volume_ml,
                start_time=when, end_time=when, notes=notes, description=description)

        return keg

    @transaction.atomic
    def connect_meter(self, tap, new_meter):
        tap = self._get_tap(tap)
        old_meter = tap.current_meter()

        if old_meter != new_meter:
            if old_meter:
                old_meter.tap = None
                old_meter.save()
            if new_meter:
                new_meter.tap = tap
                new_meter.save()

        return tap

    @transaction.atomic
    def connect_toggle(self, tap, new_toggle):
        tap = self._get_tap(tap)
        old_toggle = tap.current_toggle()

        if old_toggle != new_toggle:
            if old_toggle:
                old_toggle.tap = None
                old_toggle.save()
            if new_toggle:
                new_toggle.tap = tap
                new_toggle.save()

        return tap

    def build_stats(self, since_drink_id):
        """Rebuilds statistics starting with this drink."""
        assert since_drink_id is not None, 'No drink id.'
        with SuppressTaskErrors(self._logger):
            tasks.build_stats.delay(since_drink_id=since_drink_id)

    def _get_tap(self, keg_tap_or_meter_name):
        if isinstance(keg_tap_or_meter_name, models.KegTap):
            return keg_tap_or_meter_name
        try:
            return models.KegTap.get_from_meter_name(keg_tap_or_meter_name)
        except models.KegTap.DoesNotExist, e:
            raise BackendError('Invalid tap: %s: %s' % (repr(keg_tap_or_meter_name), e))

    def _get_sensor_from_name(self, name, autocreate=True):
        """Returns the TemperatureSensor with raw_name matching name.

        Args:
            name: The sensor's raw_name.
            autocreate: If True, create a new sensor if one does not exist.

        Returns:
            The TemperatureSensor object, or None if none exists and autocreate was
            not True.
        """
        try:
            return models.ThermoSensor.objects.get(raw_name=name)
        except models.ThermoSensor.DoesNotExist:
            if autocreate:
                sensor = models.ThermoSensor(raw_name=name, nice_name=name)
                sensor.save()
                return sensor
            else:
                return None

def get_user(user_or_username):
    """Returns the User object for the given username, or None."""
    if not user_or_username:
        return None
    if not isinstance(user_or_username, models.User):
        return models.User.objects.get(username=user_or_username)
    return user_or_username

def get_drink(drink_or_id):
    if not isinstance(drink_or_id, models.Drink):
        return models.Drink.objects.get(pk=drink_or_id)
    return drink_or_id
