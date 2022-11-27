import datetime
from util.export import (export_csv)
import requests
from requests.auth import HTTPBasicAuth


def export_all_jira_projects(atlassian_site, atlassian_user, atlassian_token, export_filename):
    start_at = 0
    max_results = 50
    first_call = True
    projects_list = []
    projects_count = 0

    print('{} - INFO - Reading Jira projects from Atlassian Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or next_page == True:
        projects_response = requests.get(
            'https://{}.atlassian.net/rest/api/3/project/search?expand=description,lead&startAt={}&maxResults={}'.format(atlassian_site, str(start_at), str(max_results)),
            auth=HTTPBasicAuth(atlassian_user, atlassian_token)
        ).json()

        number_of_results = len(projects_response)
        for project in projects_response['values']:
            projects_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'project_id': project['id'],
                'project_key': project['key'],
                'project_name': project['name'],
                'project_description': project['description'],
                'project_lead_account_id': project['lead']['accountId'],
                'projectTypeKey': project['projectTypeKey'],
                'simplified': project['simplified'],
                'style': project['style'],
                'isPrivate': project['isPrivate']
            })
            projects_count = projects_count + 1
        if "nextPage" in projects_response:
            next_page = True
        else:
            next_page = False
        start_at = start_at + max_results
        first_call = False

    print('{} - INFO - Total Jira Projects: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(projects_count)))

    export_csv(
        export_filename,
        projects_list,
        ['date', 'project_id', 'project_key', 'project_name', 'project_description', 'project_lead_account_id', 'project_type_key', 'simplified', 'style', 'is_private'],
        ['date', 'project_id', 'project_key', 'project_name', 'project_description', 'project_lead_account_id', 'projectTypeKey', 'simplified', 'style', 'isPrivate']
    )