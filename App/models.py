from django.db import models
from App import activityReport
import pandas as pd


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254,unique=True)


def handle_uploaded_file(f, szn, c_list):
    with open('static/data.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    df = pd.read_csv('static/data.csv')
    results_template = pd.read_csv('static/ReportTemplate.csv')
    report = activityReport.runActivityReport(c_list, szn, df, results_template)
    report.to_csv('static/report.csv')