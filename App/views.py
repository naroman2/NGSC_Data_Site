from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from App.forms import NewUserForm, UpdatePulseData, UploadFileForm
from django.http import HttpResponseRedirect
from App.models import handle_uploaded_file
from App.internTool import *
from App.pulseTool import *


# Create your views here.

def home(request):
    return render(request, 'App/home.html')


def about(request):
    return render(request, 'App/about.html')


def activityReport(request):
    return render(request, 'App/activityReport.html')


def internTool(request):
    return render(request, 'App/internTool.html')


def users(request):

    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return about(request)
        else:
            print('ERROR FORM INVALID')

    return render(request,'App/form.html',{'form':form})


def upload_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            szn = request.POST['season']
            c_list = ['All', request.POST['y1'], request.POST['y2'], request.POST['y3'], request.POST['y4'],
                      request.POST['t1'], request.POST['t2']]
            handle_uploaded_file(request.FILES['file'], szn, c_list)
            return render(request, 'App/activityReport.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'App/activityReport.html', {'form': form})


def activate(request):
    # run the main method in the intern tool script
    count = run()
    return render(request, 'App/internToolSubmit.html', {'count': str(count)})


def pulseUpdate(request):
    if request.method == 'POST':
        form = UpdatePulseData(request.POST, request.FILES)
        if form.is_valid():
            lag = request.POST['date_lag']
            pulse_run(7*int(lag))
            return render(request, 'App/pulseCampaignStats.html', {'form': form})
    else:
        form = UpdatePulseData()
    return render(request, 'App/pulseCampaignStats.html', {'form': form})


