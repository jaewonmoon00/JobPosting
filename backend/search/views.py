from django.shortcuts import render
from django.views import View

from .forms import SearchForm

# Create your views here.
class SearchView(View):
    form_type = SearchForm
    template_name = 'search/search-home.html'
    fields = ('search_term', 'city', 'country', 'salary_max', 'salary_min')

    def get(self, request, *args, **kwargs):
        form = self.form_type(request.GET)
        return render(request, self.template_name, {'form': form})
