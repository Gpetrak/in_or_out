from django.conf.urls import patterns, url
from crete_gis.in_or_out.views import LookupView

urlpatterns = patterns(
    'crete_gis.in_or_out.views',
    url(r'^$',  LookupView.as_view(), name='lookup'),
    )

