from storyteller.urls import urlpatterns
from django.conf.urls import url, include

from django.shortcuts import render

def test_view(request):
    pagevars = {}
    return render(request, 'testing.html', pagevars)



ex3_patterns = [


]

custom_patterns = [
    url(r'^storyteller/ex3/', include(ex3_patterns)),
    url(r'^testing/$', test_view)
]

urlpatterns = custom_patterns + urlpatterns