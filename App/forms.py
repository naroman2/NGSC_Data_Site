from django import forms
from App.models import User


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UploadFileForm(forms.Form):
    file = forms.FileField()
    CHOICES = [('1', 'Fall'), ('2', 'Spring')]
    season = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    y1 = forms.CharField(label='Year 1')
    y2 = forms.CharField(label='Year 2')
    y3 = forms.CharField(label='Year 3')
    y4 = forms.CharField(label='Year 4')
    t1 = forms.CharField(label='Transfer 1')
    t2 = forms.CharField(label='Transfer 2')


class UpdatePulseData(forms.Form):
    CHOICES = [('1', '7'), ('2', '14'), ('3', '21'), ('4', '28')]
    date_lag = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)



