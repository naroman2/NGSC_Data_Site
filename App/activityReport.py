# Nicolas Romano
# July 16, 2021
# End of Semester Activity Report Script
# This script will read in the activities data at the end of each semester
# and export a .csv file with key statistics pertaining to the data.

import pandas as pd


def runActivityReport(cohort_list, actData, results):
    #############################################
    # Setting the Cohort Labels:                #
    #############################################
    for ind in results.index:
        results["Cohort"][ind] = cohort_list[ind]

    #############################################
    # Set the cohort sizes:                     #
    #############################################
    for ind in results.index:
        results["Total # of Active Students"][ind] = (actData[actData['Cohort'] == cohort_list[ind]]['Cohort'].count())
    results["Total # of Active Students"][0] = len(actData)  # Update the total size

    #############################################
    # Total Activities Completed:               #
    #############################################
    for ind in results.index:
        results["Total # of Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]]['Activities Count'].sum()
    results["Total # of Activities completed"][0] = actData["Activities Count"].sum()

    #############################################
    # Proportion of Activities to Students:     #
    #############################################
    for ind in results.index:
        results["Proportion of Activites to Students"][ind] = round(results["Total # of Activities completed"][ind]/results["Total # of Active Students"][ind], 2)

    #############################################
    # Total Service Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Service Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]]['service count'].sum()
    results["# of Service Activities completed"][0] = actData["service count"].sum()

    #############################################
    # % completed (Service)                     #
    #############################################
    for ind in results.index:
        results["% completed (Service)"][ind] = 100*round(results["# of Service Activities completed"][ind]/results["Total # of Activities completed"][ind], 3)

    #############################################
    # Total Civ-Mil Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Civ-Mil Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]]['civ mil count'].sum()
    results["# of Civ-Mil Activities completed"][0] = actData["civ mil count"].sum()

    #############################################
    # % completed (Civ-Mil)                     #
    #############################################
    for ind in results.index:
        results["% completed (Civ-Mil)"][ind] = 100*round(results["# of Civ-Mil Activities completed"][ind]/results["Total # of Activities completed"][ind], 3)

    #############################################
    # Total Culture Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Culture Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]]['culture count'].sum()
    results["# of Culture Activities completed"][0] = actData["culture count"].sum()

    #############################################
    # % completed (Civ-Mil)                     #
    #############################################
    for ind in results.index:
        results["% completed (Culture)"][ind] = 100 * round(results["# of Culture Activities completed"][ind] / results["Total # of Activities completed"][ind], 3)

    return results



# activities = pd.read_csv('activities2.csv')
# results_template = pd.read_csv('../static/ReportTemplate.csv')
# c_list = ['All', '2', '3', '4', '5', 'T2', 'T3']
# runActivityReport(c_list, activities, results_template)



