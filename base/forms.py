from django.forms import forms
from core.models import Customuser


class userformlog(forms.Form):

    class meta:
        model=Customuser
        fields=[
            'username','password'
        ]

class userformreg(forms.Form):

    class meta:
        model=Customuser
        fields=[
            'name','username','email','password'
        ]

