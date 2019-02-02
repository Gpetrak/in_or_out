# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from crete_gis.in_or_out.forms import LookupForm
from crete_gis.in_or_out.models import *
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
        anadas2015 = form.cleaned_data['anadas2015']
        anadasmoi = form.cleaned_data['anadasmoi']
        arxaiologikoi_xwroi = form.cleaned_data['arxaiologikoi_xwroi']
        dianomi_gys_5000 = form.cleaned_data['dianomi_gys_5000']
        nautiko_oxyro = form.cleaned_data['nautiko_oxyro']
        praxeis_xar_2015 = form.cleaned_data['praxeis_xar_2015']
        sxooap_krousona = form.cleaned_data['sxooap_krousona']

        # A dictionary to store the layers that the user can check in the client side
        layer_dict = {'natura': natura, 
                      'oikismoi': oikismoi,
                      'anadas2015': anadas2015, 
                      'anadasmoi': anadasmoi,
                      'arxaiologikoi_xwroi': arxaiologikoi_xwroi,
                      'dianomi_gys_5000' : dianomi_gys_5000,
                      'nautiko_oxyro': nautiko_oxyro,
                      'praxeis_xar_2015' : praxeis_xar_2015,
                      'sxooap_krousona' : sxooap_krousona}
        # A list to store the layers that have checked from the user
        layer_checked = []
        # A list to store the resulted messages
        results = []
  
        # Get the point
        location = Point(longitude, latitude, srid=4326)

        # check if the list of regions is empty and send a message to the client
        def inform_user(data, regions, model): 
            # A list to store the results of a layer
            result = []
            information = "Υπό Ανάπτυξη"
            if not regions:
                # Build the variables that will be sent into HTML table
                # Every vaiable is a column
                answer = "Εκτός"
                region = "--"
                # database order_by query
                nearest_region = model.objects.using('datastore').distance(location).order_by('distance').first()
            #    nearest_region_obj = geometry=model.objects.using('datastore').get(name_latin=nearest_region)
            #   dist = location.distance(rearest_region_obj.geom)
                result.extend([data, answer, region, nearest_region, information])
            else:
                answer = "Εντός"
                region = regions[0]
                nearest_region = "--"
                result.extend([data, answer, region, nearest_region, information])
            return result
        
        # query the database and call inform_user in order to return the messages
        def layer(layer_name, model):
            in_out = model.objects.using('datastore').filter(geom__contains=location)
            info = inform_user(layer_name, in_out, model)
            return info

        # Convert database table names like 'hello_world' with model names like HelloWorld
        # This is a convention of django when generates models automaticaly. 
        def table_to_model(table_name):
            table_name = table_name.split('_')
            result = ""
            for i in table_name: 
            # reconstruct the string
                result += i[0].upper() + i[1:]
            return result
        
        # iterate the dict in order to store only the checked layers (when the values are True) 
        for key, value in layer_dict.iteritems():
            if value is True:
                layer_checked.append(key)
         
        for i in layer_checked:
            # because if table_name = layer_name, model_name = LayerName
            model_name_str = table_to_model(i)
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


