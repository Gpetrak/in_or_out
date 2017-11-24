from django.forms import Form, FloatField, BooleanField

class LookupForm(Form):
    latitude = FloatField()
    longitude = FloatField()
    natura = BooleanField(required=False)
    oikismoi = BooleanField(required=False)
      
