# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


ATTRS = (
    'volume_display_units',
    'temperature_display_units',
    'title',
    'background_image',
    'google_analytics_id',
    'session_timeout_minutes',
    'privacy',
    'guest_name',
    'guest_image',
    'default_user',
    'registration_allowed',
    'registration_confirmation',
    'allowed_hosts',
    'timezone',
    'hostname',
    'use_ssl',
    'check_for_updates'
)

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KegbotSite.volume_display_units'
        db.add_column(u'core_kegbotsite', 'volume_display_units',
                      self.gf('django.db.models.fields.CharField')(default='imperial', max_length=64),
                      keep_default=False)

        # Adding field 'KegbotSite.temperature_display_units'
        db.add_column(u'core_kegbotsite', 'temperature_display_units',
                      self.gf('django.db.models.fields.CharField')(default='f', max_length=64),
                      keep_default=False)

        # Adding field 'KegbotSite.title'
        db.add_column(u'core_kegbotsite', 'title',
                      self.gf('django.db.models.fields.CharField')(default='My Kegbot', max_length=64),
                      keep_default=False)

        # Adding field 'KegbotSite.background_image'
        db.add_column(u'core_kegbotsite', 'background_image',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Picture'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'KegbotSite.google_analytics_id'
        db.add_column(u'core_kegbotsite', 'google_analytics_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'KegbotSite.session_timeout_minutes'
        db.add_column(u'core_kegbotsite', 'session_timeout_minutes',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=180),
                      keep_default=False)

        # Adding field 'KegbotSite.privacy'
        db.add_column(u'core_kegbotsite', 'privacy',
                      self.gf('django.db.models.fields.CharField')(default='public', max_length=63),
                      keep_default=False)

        # Adding field 'KegbotSite.guest_name'
        db.add_column(u'core_kegbotsite', 'guest_name',
                      self.gf('django.db.models.fields.CharField')(default='guest', max_length=63),
                      keep_default=False)

        # Adding field 'KegbotSite.guest_image'
        db.add_column(u'core_kegbotsite', 'guest_image',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='guest_images', null=True, on_delete=models.SET_NULL, to=orm['core.Picture']),
                      keep_default=False)

        # Adding field 'KegbotSite.default_user'
        db.add_column(u'core_kegbotsite', 'default_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'KegbotSite.registration_allowed'
        db.add_column(u'core_kegbotsite', 'registration_allowed',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'KegbotSite.registration_confirmation'
        db.add_column(u'core_kegbotsite', 'registration_confirmation',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'KegbotSite.allowed_hosts'
        db.add_column(u'core_kegbotsite', 'allowed_hosts',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)

        # Adding field 'KegbotSite.timezone'
        db.add_column(u'core_kegbotsite', 'timezone',
                      self.gf('django.db.models.fields.CharField')(default='UTC', max_length=255),
                      keep_default=False)

        # Adding field 'KegbotSite.hostname'
        db.add_column(u'core_kegbotsite', 'hostname',
                      self.gf('django.db.models.fields.CharField')(default='localhost:8000', max_length=255),
                      keep_default=False)

        # Adding field 'KegbotSite.use_ssl'
        db.add_column(u'core_kegbotsite', 'use_ssl',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'KegbotSite.check_for_updates'
        db.add_column(u'core_kegbotsite', 'check_for_updates',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        if not db.dry_run:
            site = orm['core.KegbotSite'].objects.get(name='default')
            settings = site.settings

            for attr in ATTRS:
                setattr(site, attr, getattr(settings, attr))
            site.save()


    def backwards(self, orm):
        # Deleting field 'KegbotSite.volume_display_units'
        db.delete_column(u'core_kegbotsite', 'volume_display_units')

        # Deleting field 'KegbotSite.temperature_display_units'
        db.delete_column(u'core_kegbotsite', 'temperature_display_units')

        # Deleting field 'KegbotSite.title'
        db.delete_column(u'core_kegbotsite', 'title')

        # Deleting field 'KegbotSite.background_image'
        db.delete_column(u'core_kegbotsite', 'background_image_id')

        # Deleting field 'KegbotSite.google_analytics_id'
        db.delete_column(u'core_kegbotsite', 'google_analytics_id')

        # Deleting field 'KegbotSite.session_timeout_minutes'
        db.delete_column(u'core_kegbotsite', 'session_timeout_minutes')

        # Deleting field 'KegbotSite.privacy'
        db.delete_column(u'core_kegbotsite', 'privacy')

        # Deleting field 'KegbotSite.guest_name'
        db.delete_column(u'core_kegbotsite', 'guest_name')

        # Deleting field 'KegbotSite.guest_image'
        db.delete_column(u'core_kegbotsite', 'guest_image_id')

        # Deleting field 'KegbotSite.default_user'
        db.delete_column(u'core_kegbotsite', 'default_user_id')

        # Deleting field 'KegbotSite.registration_allowed'
        db.delete_column(u'core_kegbotsite', 'registration_allowed')

        # Deleting field 'KegbotSite.registration_confirmation'
        db.delete_column(u'core_kegbotsite', 'registration_confirmation')

        # Deleting field 'KegbotSite.allowed_hosts'
        db.delete_column(u'core_kegbotsite', 'allowed_hosts')

        # Deleting field 'KegbotSite.timezone'
        db.delete_column(u'core_kegbotsite', 'timezone')

        # Deleting field 'KegbotSite.hostname'
        db.delete_column(u'core_kegbotsite', 'hostname')

        # Deleting field 'KegbotSite.use_ssl'
        db.delete_column(u'core_kegbotsite', 'use_ssl')

        # Deleting field 'KegbotSite.check_for_updates'
        db.delete_column(u'core_kegbotsite', 'check_for_updates')




    models = {
        u'core.apikey': {
            'Meta': {'object_name': 'ApiKey'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'e1de537401e17e2505b719ef01c0c9ec'", 'unique': 'True', 'max_length': '127'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'})
        },
        u'core.authenticationtoken': {
            'Meta': {'unique_together': "(('auth_device', 'token_value'),)", 'object_name': 'AuthenticationToken'},
            'auth_device': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nice_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'token_value': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tokens'", 'null': 'True', 'to': u"orm['core.User']"})
        },
        u'core.beverage': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Beverage'},
            'abv_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'beverage_backend': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'beverage_backend_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'beverage_type': ('django.db.models.fields.CharField', [], {'default': "'beer'", 'max_length': '32'}),
            'calories_per_ml': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'carbs_per_ml': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'original_gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Picture']", 'null': 'True', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BeverageProducer']"}),
            'specific_gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'untappd_beer_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vintage_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.beverageproducer': {
            'Meta': {'ordering': "('name',)", 'object_name': 'BeverageProducer'},
            'country': ('pykeg.core.fields.CountryField', [], {'default': "'USA'", 'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_homebrew': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'origin_city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'origin_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Picture']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.controller': {
            'Meta': {'object_name': 'Controller'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'core.drink': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'Drink'},
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'drinks'", 'on_delete': 'models.PROTECT', 'to': u"orm['core.Keg']"}),
            'picture': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Picture']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'drinks'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['core.DrinkingSession']"}),
            'shout': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tick_time_series': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ticks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'drinks'", 'to': u"orm['core.User']"}),
            'volume_ml': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.drinkingsession': {
            'Meta': {'ordering': "('-start_time',)", 'object_name': 'DrinkingSession'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'volume_ml': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'core.flowmeter': {
            'Meta': {'unique_together': "(('controller', 'port_name'),)", 'object_name': 'FlowMeter'},
            'controller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meters'", 'to': u"orm['core.Controller']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tap': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'meter'", 'unique': 'True', 'null': 'True', 'to': u"orm['core.KegTap']"}),
            'ticks_per_ml': ('django.db.models.fields.FloatField', [], {'default': '5.4'})
        },
        u'core.flowtoggle': {
            'Meta': {'unique_together': "(('controller', 'port_name'),)", 'object_name': 'FlowToggle'},
            'controller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'toggles'", 'to': u"orm['core.Controller']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tap': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'toggle'", 'unique': 'True', 'null': 'True', 'to': u"orm['core.KegTap']"})
        },
        u'core.keg': {
            'Meta': {'object_name': 'Keg'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'full_volume_ml': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg_type': ('django.db.models.fields.CharField', [], {'default': "'half-barrel'", 'max_length': '32'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'served_volume_ml': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'spilled_ml': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Beverage']", 'on_delete': 'models.PROTECT'})
        },
        u'core.kegbotsite': {
            'Meta': {'object_name': 'KegbotSite'},
            'allowed_hosts': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'background_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Picture']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'check_for_updates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'epoch': ('django.db.models.fields.PositiveIntegerField', [], {'default': '105'}),
            'google_analytics_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'guest_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'guest_images'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.Picture']"}),
            'guest_name': ('django.db.models.fields.CharField', [], {'default': "'guest'", 'max_length': '63'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_setup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_checkin_response': ('pykeg.core.jsonfield.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'last_checkin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'unique': 'True', 'max_length': '64'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '63'}),
            'registration_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'registration_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_id': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'session_timeout_minutes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'temperature_display_units': ('django.db.models.fields.CharField', [], {'default': "'f'", 'max_length': '64'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'My Kegbot'", 'max_length': '64'}),
            'use_ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'volume_display_units': ('django.db.models.fields.CharField', [], {'default': "'imperial'", 'max_length': '64'})
        },
        u'core.kegtap': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'KegTap'},
            'current_keg': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'current_tap'", 'unique': 'True', 'null': 'True', 'to': u"orm['core.Keg']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'temperature_sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ThermoSensor']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'core.picture': {
            'Meta': {'object_name': 'Picture'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pictures'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.Keg']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pictures'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.DrinkingSession']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pictures'", 'null': 'True', 'to': u"orm['core.User']"})
        },
        u'core.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'allowed_hosts': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'background_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Picture']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'check_for_updates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'google_analytics_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'guest_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'guest_images_old'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.Picture']"}),
            'guest_name': ('django.db.models.fields.CharField', [], {'default': "'guest'", 'max_length': '63'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '63'}),
            'registration_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'registration_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session_timeout_minutes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': u"orm['core.KegbotSite']"}),
            'temperature_display_units': ('django.db.models.fields.CharField', [], {'default': "'f'", 'max_length': '64'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'My Kegbot'", 'max_length': '64'}),
            'use_ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'volume_display_units': ('django.db.models.fields.CharField', [], {'default': "'imperial'", 'max_length': '64'})
        },
        u'core.stats': {
            'Meta': {'unique_together': "(('drink', 'user', 'keg', 'session'),)", 'object_name': 'Stats'},
            'drink': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Drink']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_first': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'null': 'True', 'to': u"orm['core.Keg']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'null': 'True', 'to': u"orm['core.DrinkingSession']"}),
            'stats': ('pykeg.core.jsonfield.JSONField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'null': 'True', 'to': u"orm['core.User']"})
        },
        u'core.systemevent': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'SystemEvent'},
            'drink': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['core.Drink']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['core.Keg']"}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['core.DrinkingSession']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['core.User']"})
        },
        u'core.thermolog': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'Thermolog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ThermoSensor']"}),
            'temp': ('django.db.models.fields.FloatField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.thermosensor': {
            'Meta': {'object_name': 'ThermoSensor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nice_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raw_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mugshot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_mugshot'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['core.Picture']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['core']