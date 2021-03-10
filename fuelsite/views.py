from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CampaignForm, DatafileForm, HouseholdForm, OrganizationForm, AccountUserForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)

# from fuelsite.functions.py import handle_uploaded_file

# Create your views here.

def login_function(request, password):
    form_error = False
    username = request.POST['username']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        form_error = True

    return form_error



#def login_view(request):
#    form_error = False
#    if request.method == 'POST':
#        loginForm = AuthenticationForm(data=request.POST)
#        if(loginForm.is_valid()):
#            form_error = login_function(request, request.POST['password'])
#        else:
#            form_error = True
#    return render(request, 'org_data.html', {'error': form_error, "form": "login"})

def login_view(request):
    form_error = False
    if request.method == 'POST':
        loginForm = AuthenticationForm(data=request.POST)
        if(loginForm.is_valid()):
            form_error = login_function(request, request.POST['password'])
        else:
            form_error = True
    return render(request, 'org_data.html', {'error': form_error, "form": "login"})


def logout_view(request):
    logout(request)
    return redirect('/')


def login_function(request, password):
    form_error = False
    username = request.POST['username']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        form_error = True

    return form_error



def login_view(request):
    form_error = False
    if request.method == 'POST':
        loginForm = AuthenticationForm(data=request.POST)
        if(loginForm.is_valid()):
            form_error = login_function(request, request.POST['password'])
        else:
            form_error = True
    return render(request, 'org_data.html', {'error': form_error, "form": "login"})



def logout_view(request):
    logout(request)
    return redirect('/')


def create_account(request):
    form_error = False
    if request.method == 'POST':
        userCreate = AccountUserForm(request.POST or None)
        if(userCreate.is_valid()):
            userCreate.save()
            form_error = login_function(request, request.POST['password1'])
        else:
            form_error = True
    return render(request, 'org_data.html', {'error': form_error, 'form': "createAccount"})


def test_vue(request):
    return render(request, 'test.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def getForms(request, context):
    context['householdform'] = HouseholdForm(request.POST or None)
    context['datafileform'] = DatafileForm(request.POST or None)
    context['campaignform'] = CampaignForm(request.POST or None)
    context['organizationform'] = OrganizationForm(request.POST or None)
    return context

def org_data(request):

    context = {}
    getForms(request, context)

    if request.method == 'POST':
        if context['campaignform'].is_valid():
            context['campaignform'].save()
        elif context['datafileform'].is_valid():
            context['datafileform'].save()
        elif context['householdform'].is_valid():
            context['householdform'].save()
        elif context['organizationform'].is_valid():
            context['organizationform'].save()

    getForms(request, context)
    return render(request, 'org_data.html', context)

def public(request):
    return render(request, 'public.html')
