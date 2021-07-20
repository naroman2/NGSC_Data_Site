from django import forms
from App.models import User


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()
