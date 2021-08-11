# Nicolas Romano - April 26, 2021
# This Python Script will access my Mailchimp and Airtable accounts through their respective API systems.
# It will check Airtable to see what the most recently recorded campaign email record date is.
# It will then compare this with Mailchimp to see if any campaigns have been sent since that date.
# If so, the Airtable database will be updated with the new campaign data.

# Import statements for mailchimp's api
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Creating a mailchimp api client object with the correct server and api key
client = MailchimpMarketing.Client()
client.set_config({
    "api_key": "b9bf7416c06bc8d616f133072d3d43e5-us12",
    "server": "us12"
})

# Airtable API important constants:
AIRTABLE_BASE_ID = "apphONPQ0v4Kj32w8"
AIRTABLE_API_KEY = 'key03Sbgj7e4tTcj5'
AIRTABLE_TABLE_NAME = "stats"
endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
# Python Requests Headers:
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}


# Function to get campaign data for a specific campaign given its campaign id:
def retrieve(campaign_id):
    # list to store retrieved data
    ls = ["a", "b", .2, 1, 33, .9822, 12, 21, 200, "2021-09-10"]
    response = client.reports.get_campaign_report(campaign_id)
    ls[0] = response.get('id')
    ls[1] = response.get('campaign_title')
    ls[2] = round(response.get('clicks').get('click_rate'), 4)
    ls[3] = response.get('clicks').get('unique_clicks')
    ls[4] = response.get('clicks').get('clicks_total')
    ls[5] = round(response.get('opens').get('open_rate'), 4)
    ls[6] = response.get('opens').get('unique_opens')
    ls[7] = response.get('opens').get('opens_total')
    ls[8] = response.get('emails_sent')
    ls[9] = response.get('send_time')[0:10]
    return ls


# Function to upload a campaign record to mailchimp given a list of parameters
def upload(ls):
    data = {
        "records": [{
            "fields": {
                "campaign_id": ls[0],
                "campaign_title": ls[1],
                "click_rate": ls[2],
                "unique_clicks": ls[3],
                "clicks_total": ls[4],
                "open_rate": ls[5],
                "unique_opens": ls[6],
                "opens_total": ls[7],
                "emails_sent": ls[8],
                "send_time": ls[9]
            }
        }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)


# Function which finds the most recent campaign email and returns its sent date:
def max_date():
    # Gathering table records:
    params = ()
    airtable_records = []
    run = True
    while run is True:
        response = requests.get(endpoint, params=params, headers=headers)
        airtable_response = response.json()
        airtable_records += (airtable_response['records'])
        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset']),)
        else:
            run = False

    # Converting those records to a pandas dataframe
    airtable_rows = []
    airtable_index = []
    for record in airtable_records:
        airtable_rows.append(record['fields'])
        airtable_index.append(record['id'])
    df = pd.DataFrame(airtable_rows, index=airtable_index)
    df = df.set_index("campaign_id")

    # function to find the most recent campaign date:
    rd = df['send_time'].max()
    return rd


# will upload the number of new campaigns to upload:
def upload_new_campaigns(date):
    go = True
    os = 0
    while go:
        response = client.reports.get_all_campaign_reports(offset=os)
        for i in range(0, 10):
            campaign_id = response.get('reports')[i].get('id')
            print(campaign_id)
            ls = retrieve(campaign_id)
            print(ls[9])
            print(date)
            if str(ls[9]) > date:
                upload(ls)
            else:
                go = False
                break
        os = os + 10


# Executable code section:
def pulse_run(lag):
    date = max_date()
    datetime_object = datetime.strptime(date, '%Y-%m-%d')
    delay = timedelta(lag)
    upload_new_campaigns(str(datetime_object - delay))






