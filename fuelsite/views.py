from django.shortcuts import render
from django.http import HttpResponse
from .forms import CampaignForm
from .forms import DatafileForm
from .forms import HouseholdForm
from .forms import OrganizationForm

import logging

logger = logging.getLogger(__name__)

# from fuelsite.functions.py import handle_uploaded_file

# Create your views here.

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
