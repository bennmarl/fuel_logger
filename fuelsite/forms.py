from django import forms
from .models import Campaign, Datafile, Household, Organization
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UploadFileForm(forms.Form):
    title=forms.CharField(max_length=50)
    file=forms.FileField()

class CampaignForm(forms.ModelForm):
    class Meta: 
        # define fields based on database model
        model = Campaign
        fields = "__all__"
        #fields = ['time', 'public', 'town', 'name']

class DatafileForm(forms.ModelForm):
    class Meta: 
        # define fields based on database model
        model = Datafile
        fields = "__all__"

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = "__all__"

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


       