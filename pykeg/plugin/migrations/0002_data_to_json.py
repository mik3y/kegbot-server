# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from kegbot.util import kbjson

class Migration(DataMigration):

    def forwards(self, orm):
        for row in orm['plugin.PluginData'].objects.all():
            try:
                # Do nothing if already valid json.
                kbjson.loads(row.value)
            except ValueError:
                print ' ~ {} -> {}'.format(repr(row.value), repr(kbjson.dumps(row.value)))
                row.value = kbjson.dumps(row.value)
                row.save()

    def backwards(self, orm):
        pass

    models = {
        u'plugin.plugindata': {
            'Meta': {'unique_together': "(('plugin_name', 'key'),)", 'object_name': 'PluginData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'plugin_name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['plugin']
    symmetrical = True
