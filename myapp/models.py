import mongoengine as me
from django.utils import timezone

class User(me.Document):
    full_name = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    phone_number = me.StringField()
    is_admin = me.BooleanField(default=False)

class Audio(me.Document):
    name = me.StringField()
    location = me.StringField()  # File path if TTS is true
    text = me.StringField()
    user = me.ReferenceField(User)  # Reference to the User
    datetime = me.DateTimeField(default=timezone.now)
