# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from crete_gis.in_or_out.forms import LookupForm
from crete_gis.in_or_out.models import Natura
from crete_gis.in_or_out.models import Oikismoi
from django.contrib.gis.geos import Point
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.measure import D # 'D' is a shortcut for 'Distance'
from django.template import RequestContext
from django.core.serializers import serialize
import json, ast


class LookupView(FormView):
    # template that is rendered when the form is valid
    template_name = 'in_or_out/lookupresults.html'
    form_class = LookupForm
    
    def get(self, request): 
        return render_to_response('in_or_out/lookup.html', RequestContext(request))
    
    def form_valid(self, form):
        # Get data
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        # Get the model for the query
        natura = form.cleaned_data['natura']
        oikismoi = form.cleaned_data['oikismoi']
 

        # Get Point
        location = Point(longitude, latitude, srid=4326)

        # check if the list of regions is empty
        def inform_user(data, regions): 
            if not regions:
                result = u"Η τοποθεσία σας είναι εκτός περιοχής %s" % data
            else:
                result = u"Η τοποθεσία σας είναι εντός της περιοχής %s %s" % (data, regions[0])
            return result

        if natura is True:
            # Database query to detect if the location 
            # is in a regions of the models' regions 
            in_out = Natura.objects.using('datastore').filter(geom__contains=location)
            natura_result = inform_user(natura, in_out)
        if oikismoi is True:
            in_out = Oikismoi.objects.using('datastore').filter(geom__contains=location)
            oikismoi_result = inform_user(oikismoi, in_out)

        # Render the template
        return self.render_to_response({
                                  'oikismoi_result': oikismoi_result,
                                  'natura_result': natura_result,
                                  'longitude': longitude,
                                  'latitude': latitude
                                 })


