import datetime
import requests
from requests.auth import HTTPBasicAuth
from util.export import (export_csv)


def export_all_bitbucket_users(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):
    page = 1
    pagelen = 100
    number_of_results = 0
    first_call = True
    users_list = []

    print('{} - INFO - Reading Bitbucket users from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    while first_call == True or next_page == True:

        retry_for_api_ready = True
        retry_count = 0
        while retry_for_api_ready and retry_count<10:
            http_response = requests.get(
                'https://api.bitbucket.org/2.0/workspaces/{}/members?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
                auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
            )
            if http_response.status_code == 429:
                sleep(60)
                retry_count += 1
                print('{} - INFO - http response {}, wait and retry again, retry count {} for page {}...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code, str(retry_count), str(page)))
            else:
                retry_for_api_ready = False

        if http_response.status_code == 200:
            for http_response_item in http_response.json().get('values'):
                http_response_item_user = http_response_item.get('user')
                users_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'display_name': http_response_item_user.get('display_name'),
                    'type': http_response_item_user.get('type'),
                    'uuid': http_response_item_user.get('uuid'),
                    'account_id': http_response_item_user.get('account_id'),
                    'nickname': http_response_item_user.get('nickname')
                })

            number_of_results = http_response.json().get('size')

            if "next" in http_response.json():
                next_page = True
            else:
                next_page = False
            page = page + 1
        else:
            next_page = False
            print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

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

    retry_for_api_ready = True
    retry_count = 0
    while retry_for_api_ready and retry_count < 10:
        http_response = requests.get(
            'https://api.bitbucket.org/1.0/groups/{}/'.format(bitbucket_workspace),
            auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
        )
        if http_response.status_code == 429:
            sleep(60)
            retry_count += 1
            print('{} - INFO - http response {}, wait and retry again, retry count {}...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code, str(retry_count)))
        else:
            retry_for_api_ready = False

    if http_response.status_code == 200:
        for http_response_item in http_response.json():
            groups_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'auto_add': http_response_item.get('auto_add'),
                'name': http_response_item.get('name'),
                'slug': http_response_item.get('slug'),
                'permission': http_response_item.get('permission')
            })
            group_count += 1
            for http_response_item_group_member in http_response_item['members']:
                groups_members_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'group_name': http_response_item.get('name'),
                    'group_slug': http_response_item.get('slug'),
                    'is_staff': http_response_item_group_member.get('is_staff'),
                    'is_active': http_response_item_group_member.get('is_active'),
                    'nickname': http_response_item_group_member.get('nickname'),
                    'account_id': http_response_item_group_member.get('account_id'),
                    'uuid': http_response_item_group_member.get('uuid'),
                    'display_name': http_response_item_group_member.get('display_name'),
                    'is_team': http_response_item_group_member.get('is_team')
                })
                group_members_count += 1
    else:
        print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

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
