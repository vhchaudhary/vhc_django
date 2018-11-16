import pdb

from django import forms
from django.conf import settings
import requests

class DictionaryForm(forms.Form):

    word = forms.CharField(max_length=50, required=True)

    def search(self):

        result = {}
        word = self.cleaned_data['word']
        endpoint = 'https://od-api.oxforddictionaries.com/api/v1/entries/{source_lang}/{word_id}'
        url = endpoint.format(source_lang='en', word_id=word)

        headers = {'app_id': settings.OXFORD_APP_ID, 'app_key': settings.OXFORD_APP_KEY}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            result = response.json()

            result['success'] = True

        else:
            result['success'] = False

        return result
