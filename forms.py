from django.forms import Form, FloatField, BooleanField

class LookupForm(Form):
    latitude = FloatField()
    longitude = FloatField()
    natura = BooleanField(required=False)
    oikismoi = BooleanField(required=False)
    anadas2015 = BooleanField(required=False)
    anadasmoi = BooleanField(required=False) 
    arxaiologikoi_xwroi = BooleanField(required=False)
    dianomi_gys_5000 = BooleanField(required=False)
    nautiko_oxyro = BooleanField(required=False)
    praxeis_xar_2015 = BooleanField(required=False)
    sxooap_krousona = BooleanField(required=False)
