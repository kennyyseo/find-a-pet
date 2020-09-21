from django import forms


class HomeSearchForm(forms.Form):
    zip = forms.IntegerField()
