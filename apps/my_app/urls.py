from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index , name='mainPage'),
    url(r'^find_definition$', word, name="definition")
]
