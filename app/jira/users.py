import datetime
from util.export import (export_csv)
import requests
from requests.auth import HTTPBasicAuth


def export_all_jira_groups(atlassian_site, atlassian_user, atlassian_token, export_filename):

    print('{} - INFO - Reading Atlassian groups from Atlassian Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    start_at = 0
    max_results = 50
    number_of_results = 0
    first_call = True
    groups_list = []

    while first_call == True or start_at < number_of_results:
        groups_response = requests.get(
            'https://{}.atlassian.net/rest/api/3/group/bulk?startAt={}&maxResults={}'.format(atlassian_site, str(start_at), str(max_results)),
            auth=HTTPBasicAuth(atlassian_user, atlassian_token)
        ).json()

        number_of_results = int(groups_response["total"])
        for group in groups_response["values"]:
            if str(group['name']) != 'atlassian-addons':
                groups_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'name': group['name'],
                    'groupId': group['groupId']
                })
        start_at = start_at + max_results
        first_call = False

    print('{} - INFO - Total groups: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    export_csv(export_filename, groups_list, ['date', 'group_name', 'group_id'], ['date', 'name', 'groupId'])

    return groups_list


def export_all_jira_groups_members(atlassian_site, atlassian_user, atlassian_token, groups_list, export_filename):

    print('{} - INFO - Reading Atlassian groups members from Atlassian Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    groups_members_list = []

    for group in groups_list:

        start_at = 0
        max_results = 50
        number_of_results = 0
        first_call = True

        while first_call == True or start_at < number_of_results:
            #print('{} - INFO - Getting group members for group {} starting at index {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), group['name'], str(start_at)))
            group_members_response = requests.get(
                'https://{}.atlassian.net/rest/api/3/group/member?groupname={}&startAt={}&maxResults={}'.format(atlassian_site, group['name'], str(start_at), str(max_results)),
                auth=HTTPBasicAuth(atlassian_user, atlassian_token)
            ).json()

            if 'errorMessages' in group_members_response:
                print('{} - ERROR - errorMessages found for group {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), group['name']))
            else:
                number_of_results = int(group_members_response['total'])
                #print('{} - INFO - Total of {} members for Atlassian group {} starting at index {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results), group['name'], str(start_at)))
                for membership in group_members_response['values']:
                    groups_members_list.append({
                        'date': datetime.datetime.now().strftime("%Y%m%d"),
                        'groupId': group['groupId'],
                        'accountId': membership['accountId']
                    })

            start_at = start_at + max_results
            first_call = False

        print('{} - INFO - Total of {} members for Atlassian group {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results), group['name']))

    export_csv(export_filename, groups_members_list, ['date', 'group_id', 'account_id'], ['date', 'groupId', 'accountId'])


def export_all_jira_users(atlassian_site, atlassian_user, atlassian_token, export_filename):
    start_at = 0
    max_results = 50
    number_of_results = 0
    first_call = True
    users_list = []
    users_count = 0

    print('{} - INFO - Reading Atlassian users from Atlassian Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or max_results == number_of_results:
        users_response = requests.get(
            'https://{}.atlassian.net/rest/api/3/users/search?startAt={}&maxResults={}'.format(atlassian_site, str(start_at), str(max_results)),
            auth=HTTPBasicAuth(atlassian_user, atlassian_token)
        ).json()

        number_of_results = len(users_response)
        for user in users_response:
            users_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'accountId': user['accountId'],
                'accountType': user['accountType'],
                'emailAddress': user.get('emailAddress'),
                'displayName': user['displayName'],
                'active': user['active']
            })
            users_count = users_count + 1
        start_at = start_at + max_results
        first_call = False

    print('{} - INFO - Total: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(users_count)))

    export_csv(
        export_filename,
        users_list,
        ['date', 'account_id', 'account_type', 'email_address', 'display_name', 'active'],
        ['date', 'accountId', 'accountType', 'emailAddress', 'displayName', 'active']
    )
