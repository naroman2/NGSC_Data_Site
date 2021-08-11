# Nicolas Romano
# July 16, 2021
# End of Semester Activity Report Script
# This script will read in the activities data at the end of each semester
# and export a .csv file with key statistics pertaining to the data.

import pandas as pd


def runActivityReport(cohort_list, szn, actData, results):
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
        results["Total # of Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]][
            'Activities Count'].sum()
    results["Total # of Activities completed"][0] = actData["Activities Count"].sum()

    #############################################
    # Proportion of Activities to Students:     #
    #############################################
    for ind in results.index:
        results["Proportion of Activites to Students"][ind] = round(
            results["Total # of Activities completed"][ind] / results["Total # of Active Students"][ind], 2)

    #############################################
    # Total Service Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Service Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]][
            'service count'].sum()
    results["# of Service Activities completed"][0] = actData["service count"].sum()

    #############################################
    # % completed (Service)                     #
    #############################################
    for ind in results.index:
        results["% completed (Service)"][ind] = 100 * round(
            results["# of Service Activities completed"][ind] / results["Total # of Activities completed"][ind], 3)

    #############################################
    # Total Civ-Mil Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Civ-Mil Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]][
            'civ mil count'].sum()
    results["# of Civ-Mil Activities completed"][0] = actData["civ mil count"].sum()

    #############################################
    # % completed (Civ-Mil)                     #
    #############################################
    for ind in results.index:
        results["% completed (Civ-Mil)"][ind] = 100 * round(
            results["# of Civ-Mil Activities completed"][ind] / results["Total # of Activities completed"][ind], 3)

    #############################################
    # Total Culture Completed:                  #
    #############################################
    for ind in results.index:
        results["# of Culture Activities completed"][ind] = actData[actData['Cohort'] == cohort_list[ind]][
            'culture count'].sum()
    results["# of Culture Activities completed"][0] = actData["culture count"].sum()

    #############################################
    # % completed (Civ-Mil)                     #
    #############################################
    for ind in results.index:
        results["% completed (Culture)"][ind] = 100 * round(
            results["# of Culture Activities completed"][ind] / results["Total # of Activities completed"][ind], 3)

    #############################################
    # LEVELS Data Frames:                       #
    #############################################
    # function to be used in attendance computation for levels
    def att(val):
        return val.lower() == ('yes' or 'excused')

    # List of boolean conditions to check when computing levels
    if szn == 1:    # fall
        conditions = [(actData['service count'] >= 2), (actData['civ mil count'] >= 1), (actData['culture count'] >= 1),
                      (actData['Retreat'].apply(lambda val: att(val))),
                      (actData['MT KIckoff'].apply(lambda val: att(val)))]
    else:
        conditions = [(actData['service count'] >= 2), (actData['civ mil count'] >= 1), (actData['culture count'] >= 1),
                      (actData['OL Spring'].apply(lambda val: att(val))),
                      (actData['MT Summit'].apply(lambda val: att(val)))]

    L1 = actData.loc[conditions[0] & conditions[1] & conditions[2] & conditions[3] & conditions[4]]
    L2 = actData.loc[conditions[0] & conditions[1] & conditions[3] & conditions[4]]
    L3 = actData.loc[conditions[0] & conditions[1] & conditions[2]]
    L4 = actData.loc[conditions[1] & conditions[2] & conditions[3] & conditions[4]]
    L5 = actData.loc[conditions[0] & conditions[2] & conditions[3] & conditions[4]]

    #############################################
    # LEVEL 1                                   #
    #############################################
    for ind in results.index:
        count = len(L1[L1['Cohort'] == cohort_list[ind]]['Cohort'])
        size = results["Total # of Active Students"][ind]
        results["Level I (%)"][ind] = 100 * round(count / size, 3)
    size = results["Total # of Active Students"][0]
    results['Level I (%)'][0] = 100 * round(len(L1) / size, 3)

    #############################################
    # LEVEL 2                                   #
    #############################################
    for ind in results.index:
        count = len(L2[L2['Cohort'] == cohort_list[ind]]['Cohort'])
        size = results["Total # of Active Students"][ind]
        results["Level II (%)"][ind] = 100 * round(count / size, 3)
    size = results["Total # of Active Students"][0]
    results['Level II (%)'][0] = 100 * round(len(L2) / size, 3)

    #############################################
    # LEVEL 3                                   #
    #############################################
    for ind in results.index:
        count = len(L3[L3['Cohort'] == cohort_list[ind]]['Cohort'])
        size = results["Total # of Active Students"][ind]
        results["Level III (%)"][ind] = 100 * round(count / size, 3)
    size = results["Total # of Active Students"][0]
    results['Level III (%)'][0] = 100 * round(len(L3) / size, 3)

    #############################################
    # LEVEL 4                                   #
    #############################################
    for ind in results.index:
        count = len(L4[L4['Cohort'] == cohort_list[ind]]['Cohort'])
        size = results["Total # of Active Students"][ind]
        results["Level IV (%)"][ind] = 100 * round(count / size, 3)
    size = results["Total # of Active Students"][0]
    results['Level IV (%)'][0] = 100 * round(len(L4) / size, 3)

    #############################################
    # LEVEL 5                                   #
    #############################################
    for ind in results.index:
        count = len(L5[L5['Cohort'] == cohort_list[ind]]['Cohort'])
        size = results["Total # of Active Students"][ind]
        results["Level V (%)"][ind] = 100 * round(count / size, 3)
    size = results["Total # of Active Students"][0]
    results['Level V (%)'][0] = 100 * round(len(L5) / size, 3)

    #############################################
    # Computing Level Differences:              #
    #############################################
    for ind in results.index:
        results['% difference between Level I and Level II'][ind] = results['Level II (%)'][ind] - \
                                                                    results['Level I (%)'][ind]
        results['% difference between Level I and Level III'][ind] = results['Level III (%)'][ind] - \
                                                                     results['Level I (%)'][ind]
        results['% difference between Level I and Level IV'][ind] = results['Level IV (%)'][ind] - \
                                                                    results['Level I (%)'][ind]
        results['% difference between Level I and Level V'][ind] = results['Level V (%)'][ind] - \
                                                                   results['Level I (%)'][ind]
    return results


# activities = pd.read_csv('activities2.csv')
# results_template = pd.read_csv('../static/ReportTemplate.csv')
# c_list = ['All', '2', '3', '4', '5', 'T2', 'T3']
# season = 'fall'
# res = runActivityReport(c_list, season, activities, results_template)
# res.to_csv('results2.csv')
