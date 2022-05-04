from django.forms import Form, EmailField, CharField, URLField, FloatField, Textarea
from .models import Battle


class ContactForm(Form):
    user_email = EmailField(label='Your email address', required=True)
    battle_name = CharField(label='Battle Name', required=True)
    battle_link = URLField(label='A link to the battle\'s Wikipedia page', required=True)
    battle_date = CharField(label='The approximate date of the battle', required=True)
    battle_latitude = FloatField(label='The battle\'s latitude in decimal coordinates', required=True)
    battle_longitude = FloatField(label='The battle\'s longitude in decimal coordinates', required=True)
    message = CharField(label='Any additional information you\'d like to add', widget=Textarea, required=False)
