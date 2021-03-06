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

from django.db import models
from kegbot.util import kbjson
from pykeg.core.jsonfield import JSONField

class PluginData(models.Model):
    plugin_name = models.CharField(max_length=127,
        help_text='Plugin short name')
    key = models.CharField(max_length=127)
    value = JSONField(dump_kwargs={'cls': kbjson.JSONEncoder})

    class Meta:
        unique_together = ('plugin_name', 'key')
