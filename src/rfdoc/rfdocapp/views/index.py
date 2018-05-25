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

from django.shortcuts import render_to_response

from rfdoc.rfdocapp.models import Library
from rfdoc.rfdocapp.views.search import SearchForm


def index(request):
    libs = None
    versions = None
    if request.GET.get('sort') == 'version':
        versions = Library.objects.values('version').distinct()
        for version in versions:
            version['libs'] = [lib.name for lib in Library.objects.filter(version=version['version'])]
    else:
        libs = Library.objects.values('name').distinct()
        for lib in libs:
            versioned_libs = Library.objects.filter(name=lib['name'])
            if len(versioned_libs) > 1:
                lib['versions'] = [library.version for library in versioned_libs]
    return render_to_response('index.html', {
        'libs': libs,
        'versions': versions,
        'form': SearchForm()
        }
    )
