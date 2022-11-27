import datetime
import requests
from requests.auth import HTTPBasicAuth
from util.export import (export_csv)


def export_all_bitbucket_users(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):
    page = 1
    pagelen = 50
    number_of_results = 0
    first_call = True
    users_list = []

    print('{} - INFO - Reading Bitbucket users from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or next_page == True:
        users_response = requests.get(
            'https://api.bitbucket.org/2.0/workspaces/{}/members?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
            auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
        ).json()

        number_of_results = users_response['size']
        for user in users_response['values']:
            users_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'display_name': user['user']['display_name'],
                'type': user['user']['type'],
                'uuid': user['user']['uuid'],
                'account_id': user['user']['account_id'],
                'nickname': user['user']['nickname']
            })
        if "next" in users_response:
            next_page = True
        else:
            next_page = False
        page = page + 1
        first_call = False

    print('{} - INFO - Total users: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    export_csv(
        export_filename,
        users_list,
        ['date', 'display_name', 'type', 'uuid', 'account_id', 'nickname'],
        ['date', 'display_name', 'type', 'uuid', 'account_id', 'nickname']
    )


def export_all_bitbucket_groups_and_members(bitbucket_workspace, bitbucket_user, bitbucket_token, groups_export_filename, groups_members_export_filename):
    groups_list = []
    groups_members_list = []
    group_count = 0
    group_members_count = 0

    print('{} - INFO - Reading Bitbucket groups and members from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    groups_response = requests.get(
        'https://api.bitbucket.org/1.0/groups/{}/'.format(bitbucket_workspace),
        auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
    ).json()

    for group in groups_response:
        groups_list.append({
            'date': datetime.datetime.now().strftime("%Y%m%d"),
            'auto_add': group['auto_add'],
            'name': group['name'],
            'slug': group['slug'],
            'permission': group['permission']
        })
        group_count = group_count + 1
        for group_member in group['members']:
            groups_members_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'group_name': group['name'],
                'group_slug': group['slug'],
                'is_staff': group_member['is_staff'],
                'is_active': group_member['is_active'],
                'nickname': group_member['nickname'],
                'account_id': group_member['account_id'],
                'uuid': group_member['uuid'],
                'display_name': group_member['display_name'],
                'is_team': group_member['is_team']
            })
            group_members_count = group_members_count + 1

    print('{} - INFO - Total groups: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(group_count)))
    print('{} - INFO - Total groups memberships: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(group_members_count)))

    export_csv(
        groups_export_filename,
        groups_list,
        ['date', 'auto_add', 'name', 'slug', 'permission'],
        ['date', 'auto_add', 'name', 'slug', 'permission']
    )

    export_csv(
        groups_members_export_filename,
        groups_members_list,
        ['date', 'group_name', 'group_slug', 'is_staff', 'is_active','nickname','account_id','uuid','display_name','is_team'],
        ['date', 'group_name', 'group_slug', 'is_staff', 'is_active','nickname','account_id','uuid','display_name','is_team']
    )
