import pandas as pd
import requests
from datetime import datetime

# Student Tracking Airtable Info:
STUDENT_TRACKING_BASE_ID = "appozZXIwbL8OKzY0"
MY_API_KEY = 'key03Sbgj7e4tTcj5'
STUDENT_TRACKING_TABLE_NAME = "Internships"
STUDENT_TRACKING_ENDPOINT = f'https://api.airtable.com/v0/{STUDENT_TRACKING_BASE_ID}/{STUDENT_TRACKING_TABLE_NAME}'
# Python Requests Headers:
airtable_headers = {
    "Authorization": f"Bearer {MY_API_KEY}",
    "Content-Type": "application/json"
}

# Student Tracking Airtable Info:
STUDENT_TRACKING_BASE_ID = "apprcAWeIj0gckJaS"
INTERNSHIPS_TABLE_NAME = "NGSC Internships Database"
INTERNSHIPS_ENDPOINT = f'https://api.airtable.com/v0/{STUDENT_TRACKING_BASE_ID}/{INTERNSHIPS_TABLE_NAME}'


# function to return the data from an Airtable Table:
def airtableToPd(endpoint):
    params = ()
    airtable_records = []
    run = True
    while run is True:
        response = requests.get(endpoint, params=params, headers=airtable_headers)
        airtable_response = response.json()
        airtable_records += (airtable_response['records'])
        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset']),)
        else:
            run = False
    airtable_rows = []
    airtable_index = []
    for record in airtable_records:
        airtable_rows.append(record['fields'])
        airtable_index.append(record['id'])
    df = pd.DataFrame(airtable_rows, index=airtable_index)
    return df


# Really Long function to ensure that all mission categories are labeled the same as the airtable tags:
def formatMission(mission):
    if 'Access' in mission:
        return "Access to Healthcare"
    elif 'Animal' in mission:
        return 'Animal Rights'
    elif 'Civic' in mission:
        return 'Civic Engagement'
    elif 'Criminal' in mission:
        return 'Criminal Justice & Security'
    elif 'Cultural' in mission:
        return 'Cultural & Global Equality'
    elif 'Disabilities' in mission:
        return 'Disabilities & Empowerment'
    elif 'Policy' in mission:
        return 'Education & Policy'
    elif 'Education' in mission:
        return 'Education'
    elif 'Energy' in mission:
        return 'Energy and Climate Sustainability'
    elif 'Environment' in mission:
        return 'Environmental Sustainability'
    elif 'Gender' in mission:
        return 'Gender Equality'
    elif 'Homelessness' in mission:
        return 'Homelessness'
    elif 'Human Trafficking' in mission:
        return 'Human Trafficking'
    elif 'Hunger' in mission:
        return 'Hunger & Nutrition'
    elif 'Immigration' in mission:
        return 'Immigration, Refugees and Migrants'
    elif 'Mental' in mission:
        return 'Racial & LGBTQ+ Equality'
    elif 'Public' in mission:
        return 'Public Health'
    elif 'Racial' in mission:
        return 'Animal Rights'
    elif 'Science' in mission:
        return 'Science Tech & Innovation'
    elif 'Sexual' in mission:
        return 'Sexual & Domestic Violence'
    elif 'Sustainability' in mission:
        return 'Sustainability'
    elif 'Veterans' in mission:
        return 'Veterans Healthcare & Services'
    elif 'Water' in mission:
        return 'Water Access and Sustainability'
    elif 'Animal' in mission:
        return 'Animal Rights'
    elif 'Youth' in mission:
        return 'Youth Development'


# This function will take in a list and upload a record to the storyViewer Airtable table:
def uploadRecord(ls):
    # Data dictionary to upload:
    data = {
        "records": [
            {
                "fields": {
                    "Organization Name": ls[0],
                    "Sector": ls[1],
                    "School / College of NGSC Member": ls[2],
                    "Organization Website": ls[3],
                    "Social Mission Topic": ls[4],
                    "Internship Description": ls[5],
                    "Major/Minor": ls[6],
                    "Type": 'Completed by NGSC member',
                    "Contact Info": ls[7],
                    "Internship Type": ls[8]
                }
            }
        ]
    }
    # Creates a new record:
    r = requests.post(INTERNSHIPS_ENDPOINT, json=data, headers=airtable_headers)
    if (r.status_code == 200):
        return 1
    else:
        return 0


def uploadDf(df):
    uploadCount = 0
    for ind in df.index:
        # Creating the array of size 8:
        ls = ['test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test']
        # Filling the Array:
        ls[0] = str(df['Organization Name'][ind])
        ls[1] = str(df['Sector'][ind])
        ls[2] = str(df['College (from ASURITE ID)'][ind])[2:-2]
        ls[3] = str(df['Organization Website'][ind])
        ls[4] = [str(df['Social Mission'][ind])]
        ls[5] = str(df['Internship Description'][ind])
        ls[6] = str(df['Major/Minor'][ind])
        if str(df['Would you be willing to share with other students about this internship experience?'][ind]) == 'Yes':
            ls[7] = str(df['First Name'][ind]) + ' ' + str(df['Last Name'][ind]) + ' - ' + str(df['Email'][ind])
        else:
            ls[7] = ''
        if str(df['Type'][ind]) in ['Traditional Internship', 'Project-based Internship', 'COVID-19 Response Team']:
            ls[8] = str(df['Type'][ind])
        else:
            ls[8] = 'Traditional Internship'
        uploadCount += uploadRecord(ls)
    return uploadCount


def run():
    # Grabbing all internships data in the student tracking table:
    all_internships = airtableToPd(STUDENT_TRACKING_ENDPOINT)
    # Getting Rid of Internships without nans for their end dates and social missions:
    all_internships = all_internships.dropna(subset=['End Date', 'Social Mission'])
    # Lambda Function to convert objects to DateTime form:
    all_internships["End Date 2"] = all_internships["End Date"].apply(lambda t: datetime.strptime(t, '%Y-%m-%d'))
    min_date = datetime.strptime('1/1/2020', '%m/%d/%Y')
    all_internships = all_internships[all_internships["End Date 2"] > min_date]

    all_internships['Social Mission'] = all_internships['Social Mission'].apply(lambda x: formatMission(x))
    internships_base = airtableToPd(INTERNSHIPS_ENDPOINT)

    drop_indexes = []
    for i in all_internships.index:
        already_logged = False
        for j in internships_base.index:
            if (all_internships['Organization Name'][i] == internships_base['Organization Name'][j]) and \
                    (all_internships['Internship Description'][i] == internships_base['Internship Description'][j]):
                already_logged = True
        if already_logged:
            drop_indexes.append(i)

    all_internships = all_internships.drop(drop_indexes)

    return uploadDf(all_internships)

