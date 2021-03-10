from django import forms
from django.conf import settings
from .models import Campaign, Datafile, Household, AccountUser
from organizations.models import Organization, OrganizationUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.models import Site
from organizations.backends import invitation_backend
from organizations.backends.forms import UserRegistrationForm
#from partners.models import PartnerUser


#class UploadFileForm(forms.Form):
#    title=forms.charfield(max_length=50)
#    file=forms.filefield()

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

# Organization

class RegistrationForm(UserRegistrationForm):
    """
    Form class that allows a user to register after clicking through an
    invitation.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm or not password:
            raise forms.ValidationError("Your password entries must match")
        return super(RegistrationForm, self).clean()


class AccountUserForm(forms.ModelForm):
    #Form class for editing OrganizationUsers *and* the linked user model.
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        exclude = ('user', 'is_admin')
        model = AccountUser

    def __init__(self, *args, **kwargs):
        super(AccountUserForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        """
        This method saves changes to the linked user model.
        """
        if self.instance.pk is None:
            site = Site.objects.get(pk=settings.SITE_ID)
            self.instance.user = invitation_backend().invite_by_email(
                    self.cleaned_data['email'],
                    **{'first_name': self.cleaned_data['first_name'],
                        'last_name': self.cleaned_data['last_name'],
                        'organization': self.cleaned_data['organization'],
                        'domain': site})
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.save()
        return super(AccountUserForm, self).save(*args, **kwargs)

class OrganizationAddForm(forms.ModelForm):
    """
    Form class for creating a new organization, complete with new owner, including a
    User instance, OrganizationUser instance, and OrganizationOwner instance.
    """

    email = forms.EmailField(
        max_length=75, help_text=("The email address for the account owner")
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        exclude = ("users", "is_active")

    def save(self, **kwargs):
        """
        Create the organization, then get the user, then make the owner.
        """
        is_active = True
        try:
            user = get_user_model().objects.get(email=self.cleaned_data["email"])
        except get_user_model().DoesNotExist:
            # TODO(bennylope): look into hooks for alt. registration systems here
            user = invitation_backend().invite_by_email(
                self.cleaned_data["email"],
                **{
                    "domain": get_current_site(self.request),
                    "organization": self.cleaned_data["name"],
                    "sender": self.request.user,
                    "created": True,
                }
            )
            is_active = False
        return create_organization(
            user,
            self.cleaned_data["name"],
            self.cleaned_data["slug"],
            is_active=is_active,
        )