from django.contrib import admin
from django.forms import ModelForm
from floppyforms.gis import PointWidget, BaseGMapWidget

class CustomPointWidget(PointWidget, BaseGMapWidget):

    class Media:

        js = ('/home/gpetr/venv_2.7/geonode/geonode/static_root/floppyforms/js',)


