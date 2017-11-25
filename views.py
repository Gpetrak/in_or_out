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
from django.db.models.loading import get_model
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
        # A dictionary to store the layers that the user can check in the client side
        layer_dict = {'natura': natura, 'oikismoi': oikismoi}
        # A list to store the layers that have checked from the user
        layer_checked = []
        # A list to store the resulted messages
        results = []
 

        # Get Point
        location = Point(longitude, latitude, srid=4326)

        # check if the list of regions is empty and send a message to the client
        def inform_user(data, regions, model): 
            if not regions:
                nearest_region = model.objects.using('datastore').distance(location).order_by('distance').first()
                result = u"Η τοποθεσία σας είναι εκτός περιοχής %s. Η πλησιέστερη περιοχή %s είναι η %s" % (data, data, nearest_region)
            else:
                result = u"Η τοποθεσία σας είναι εντός της περιοχής %s %s" % (data, regions[0])
            return result
        
        # query the database and call inform_user in order to return the messages
        def layer(layer_name, model):
            in_out = model.objects.using('datastore').filter(geom__contains=location)
            info = inform_user(layer_name, in_out, model)
            return info
        
        # iterate the dict in order to store only the checked layers (when the values are True) 
        for key, value in layer_dict.iteritems():
            if value is True:
                layer_checked.append(key)
         
        for i in layer_checked:
            # because if layer = natura, model_name = Natura
            model_name_str = i.capitalize()
            # a method to return the interested model
            model_name = get_model('in_or_out', model_name_str)
            # store into results list the messages that layer function returns
            results.append(layer(i, model_name)) 
           
                 

        # Render the template
        return self.render_to_response({
                                  'results': results,
                                  'longitude': longitude,
                                  'latitude': latitude
                                 })


