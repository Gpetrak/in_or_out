from django.contrib import admin
from geonode.in_or_out.models import Loc
from django.forms import ModelForm
from floppyforms.gis import PointWidget, BaseGMapWidget

class CustomPointWidget(PointWidget, BaseGMapWidget):

    class Media:

        js = ('/home/gpetr/venv_2.7/geonode/geonode/static_root/floppyforms/js',)

class LocAdminForm(ModelForm):
    class Meta:
        model = Loc
        fields = ['name', 'location']
        widgets = {
            'location': CustomPointWidget()
    }

class LocAdmin(admin.ModelAdmin):
    form = LocAdminForm

admin.site.register(Loc, LocAdmin)
