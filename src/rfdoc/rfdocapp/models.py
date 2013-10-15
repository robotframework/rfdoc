# Copyright 2009-2013 Nokia Siemens Networks Oyj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=80)
    doc = models.TextField(verbose_name='Documentation')
    version = models.CharField(max_length=20, default='<unknown>')

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    library = models.ForeignKey(Library)
    name = models.CharField(max_length=80)
    doc = models.TextField(verbose_name='Documentation')
    args = models.CharField(max_length=200, verbose_name='Arguments',
                            help_text='Use format: <em>arg1, arg2=default</em>')

    def __unicode__(self):
        return self.name


class Init(models.Model):
    library = models.ForeignKey(Library)
    name = '<init>'
    doc = models.TextField(verbose_name='Documentation')
    args = models.CharField(max_length=200, verbose_name='Arguments',
                            help_text='Use format: <em>arg1, arg2=default</em>')

    def __unicode__(self):
        return self.name

