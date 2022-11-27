import datetime
from util.export import (export_csv)
import requests
from requests.auth import HTTPBasicAuth


def export_all_confluence_spaces(atlassian_site, atlassian_user, atlassian_token, export_filename):
    start_at = 0
    max_results = 50
    number_of_results = 0
    first_call = True
    spaces_list = []
    spaces_count = 0

    print('{} - INFO - Reading Confluence spaces from Atlassian Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or max_results == number_of_results:
        spaces_response = requests.get(
            'https://{}.atlassian.net/wiki/rest/api/space?start={}&limit={}'.format(atlassian_site, str(start_at), str(max_results)),
            auth=HTTPBasicAuth(atlassian_user, atlassian_token)
        ).json()

        number_of_results = len(spaces_response['results'])
        for project in spaces_response['results']:
            spaces_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'space_id': project['id'],
                'space_key': project['key'],
                'space_name': project['name'],
                'space_type': project['type'],
                'status': project['status']
            })
            spaces_count = spaces_count + 1
        start_at = start_at + max_results
        first_call = False

    print('{} - INFO - Total Confluence spaces: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(spaces_count)))

    export_csv(
        export_filename,
        spaces_list,
        ['date', 'space_id', 'space_key', 'space_name', 'space_type', 'status'],
        ['date', 'space_id', 'space_key', 'space_name', 'space_type', 'status']
    )