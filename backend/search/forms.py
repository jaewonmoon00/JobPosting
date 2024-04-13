from django import forms

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=False) # default value is ''
    country = forms.CharField(max_length=100, required=True)
    salary_min = forms.IntegerField(min_value=0, required=False) # default value is None
    salary_max = forms.IntegerField(min_value=0, required=False) # default value is None