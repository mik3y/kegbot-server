from django import forms

from pykeg.core import models

ALL_TAPS = models.KegTap.objects.all()
ALL_SIZES = models.KegSize.objects.all()
ALL_BEER_TYPES = models.BeerType.objects.all().order_by('name')
ALL_KEGS = models.Keg.objects.all()

class GeneralSettingsForm(forms.Form):
  name = forms.CharField(help_text='Name of this Kegbot system')

class ChangeKegForm(forms.Form):
  keg_size = forms.ModelChoiceField(queryset=ALL_SIZES,
      empty_label=None,
      help_text='Size of the new keg')

  beer_type = forms.ModelChoiceField(queryset=ALL_BEER_TYPES,
      empty_label=None,
      help_text='Choose existing type')

  cost = forms.FloatField(required=False, min_value=0,
      help_text='Price paid (optional)')
  description = forms.CharField(required=False,
      help_text='Public description of this specific keg (optional)')

class TapForm(forms.ModelForm):
  class Meta:
    model = models.KegTap

class KegHiddenSelectForm(forms.Form):
  keg = forms.ModelChoiceField(queryset=ALL_KEGS, widget=forms.HiddenInput)

class TapForm(forms.ModelForm):
  class Meta:
    model = models.KegTap
    fields = ('name', 'meter_name', 'relay_name', 'description',
        'temperature_sensor', 'ml_per_tick')

  def __init__(self, *args, **kwargs):
    site = kwargs.pop('site', None)
    super(TapForm, self).__init__(*args, **kwargs)
    self.fields['temperature_sensor'].queryset = models.ThermoSensor.objects.filter(site=site)
    self.fields['temperature_sensor'].empty_label = 'No sensor.'

class SiteSettingsForm(forms.ModelForm):
  class Meta:
    model = models.SiteSettings
    fields = (
        'title',
        'description',
        'privacy',
        'display_units',
        'event_web_hook',
        'session_timeout_minutes',
        'google_analytics_id',
        'guest_name',
        'guest_image',
        'default_user',
        'registration_allowed',
        'registration_confirmation',
        'allowed_hosts',
    )

#BeerTypeFormSet = inlineformset_factory(models.Brewer, models.BeerType)

class TweetForm(forms.Form):
  tweet = forms.CharField(max_length=140, required=True)