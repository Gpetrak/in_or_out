from django.conf.urls import patterns, url
from geonode.in_or_out.views import LookupView

urlpatterns = patterns(
    'geonode.in_or_out.views',
    url(r'^$',  LookupView.as_view(), name='lookup'),
    )

