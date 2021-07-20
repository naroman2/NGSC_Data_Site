from django.shortcuts import render
from django.http import HttpResponse
from App.forms import NewUserForm
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from App.models import handle_uploaded_file


# Create your views here.
def home(request):
    return render(request, 'App/home.html')


def about(request):
    return render(request, 'App/about.html')


def activityReport(request):
    return render(request, 'App/activityReport.html')


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
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'App/activityReport.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'App/activityReport.html', {'form': form})

