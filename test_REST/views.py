import pdb

from django.shortcuts import render
from .forms import DictionaryForm


def oxford(request):

    result = {}


    if 'word' in request.GET:
        form = DictionaryForm(request.GET)

        if form.is_valid():
            result = form.search()

    else:
        form = DictionaryForm()

    return render(request, 'test_rest/oxford.html', {'form': form, 'search_result': result})
