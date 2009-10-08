# Copyright 2009 Nokia Siemens Networks Oyj
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
from django import forms
from django.db.models import Q

from rfdocapp.models import Keyword


def search(request):
    search_performed = False
    kws = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['search_term']
            filter = Q(name__icontains=term)
            if form.cleaned_data['include_doc']:
                filter = filter | Q(doc__icontains=term)
            kws = Keyword.objects.filter(filter) 
            search_performed = True
    else:
        form = SearchForm()
    return render_to_response('search.html', {'form': form, 'kws': kws,
                                              'search_performed': search_performed})


class SearchForm(forms.Form):
    search_term = forms.CharField() 
    include_doc = forms.BooleanField(required=False)

