import datetime
import requests
from requests.auth import HTTPBasicAuth
from util.export import (export_csv)
from time import sleep
import os

def export_all_bitbucket_projects(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):
    page = 1
    pagelen = 50
    number_of_results = 0
    first_call = True
    next_page = False
    projects_list = []

    print('{} - INFO - Reading Bitbucket projects from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    while first_call == True or next_page == True:

        retry_for_api_ready = True
        retry_count = 0
        while retry_for_api_ready and retry_count<10:
            http_response = requests.get(
                'https://api.bitbucket.org/2.0/workspaces/{}/projects?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
                auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
            )
            if http_response.status_code == 429:
                sleep(60)
                retry_count += 1
                print('{} - INFO - http response {}, wait and retry again, retry count {} for page {}...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code, str(retry_count), str(page)))
            else:
                retry_for_api_ready = False

        if http_response.status_code == 200:
            number_of_results = http_response.json().get('size')
            for http_response_item in http_response.json()['values']:
                projects_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'project_key': http_response_item.get('key'),
                    'project_uuid': http_response_item.get('uuid'),
                    'project_name': http_response_item.get('name'),
                    'is_private': http_response_item.get('is_private'),
                    'description': http_response_item.get('description'),
                    'created_on': http_response_item.get('created_on'),
                    'updated_on': http_response_item.get('updated_on'),
                    'has_publicly_visible_repos': http_response_item.get('has_publicly_visible_repos')
                })
            if "next" in http_response.json():
                next_page = True
            else:
                next_page = False
            page = page + 1
        else:
            next_page = False
            print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

        first_call = False

    print('{} - INFO - Total projects: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    export_csv(
        export_filename,
        projects_list,
        ['date', 'project_key', 'project_uuid', 'project_name', 'is_private', 'description', 'created_on', 'updated_on', 'has_publicly_visible_repos'],
        ['date', 'project_key', 'project_uuid', 'project_name', 'is_private', 'description', 'created_on', 'updated_on', 'has_publicly_visible_repos']
    )


def export_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):

    repos_list = get_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token)

    export_csv(
        export_filename,
        repos_list,
        ['date', 'project_key', 'project_uuid', 'project_name', 'repo_name', 'repo_slug', 'description', 'is_private', 'fork_policy', 'created_on', 'updated_on', 'size', 'has_issues', 'has_wiki', 'uuid'],
        ['date', 'project_key', 'project_uuid', 'project_name', 'repo_name', 'repo_slug', 'description', 'is_private', 'fork_policy', 'created_on', 'updated_on', 'size', 'has_issues', 'has_wiki', 'uuid']
    )

    return repos_list


def get_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token):
    page = 1
    pagelen = 100
    number_of_results = 0
    first_call = True
    next_page = False
    repos_list = []

    print('{} - INFO - Reading Bitbucket repos from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    while first_call == True or next_page == True:

        retry_for_api_ready = True
        retry_count = 0
        while retry_for_api_ready and retry_count<10:
            http_response = requests.get(
                'https://api.bitbucket.org/2.0/repositories/{}/?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
                auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
            )
            if http_response.status_code == 429:
                sleep(60)
                retry_count += 1
                print('{} - INFO - http response {}, wait and retry again, retry count {} for page {}...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code, str(retry_count), str(page)))
            else:
                retry_for_api_ready = False

        if http_response.status_code == 200:
            number_of_results = http_response.json().get('size')
            for http_response_item in http_response.json().get('values'):
                repos_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'project_key': http_response_item['project']['key'],
                    'project_uuid': http_response_item['project']['uuid'],
                    'project_name': http_response_item['project']['name'],
                    'repo_name': http_response_item.get('name'),
                    'repo_slug': http_response_item.get('slug'),
                    'description': http_response_item.get('description'),
                    'is_private': http_response_item.get('is_private'),
                    'fork_policy': http_response_item.get('fork_policy'),
                    'created_on': http_response_item.get('created_on'),
                    'updated_on': http_response_item.get('updated_on'),
                    'size': http_response_item.get('size'),
                    'has_issues': http_response_item.get('has_issues'),
                    'has_wiki': http_response_item.get('has_wiki'),
                    'uuid': http_response_item.get('uuid')
                })
            if "next" in http_response.json():
                next_page = True
            else:
                next_page = False
            page = page + 1
        else:
            next_page = False
            print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

        first_call = False

    print('{} - INFO - Total repos: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    return repos_list


def export_all_bitbucket_repos_commits(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):

    repos_list = get_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token)

    repos_commits_list = []

    print('{} - INFO - Reading Bitbucket repos commits from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    for repo in repos_list:
        repo_commits_list = get_bitbucket_repo_commits(bitbucket_workspace, bitbucket_user, bitbucket_token, repo['repo_name'], repo['repo_slug'])
        repos_commits_list.extend(repo_commits_list)

    export_csv(
        export_filename,
        repos_commits_list,
        ['date', 'repo_name', 'repo_slug', 'commit_type', 'commit_hash', 'commit_date', 'commit_author_type', 'commit_author_raw', 'commit_user_uuid', 'commit_user_account_id', 'commit_user_nickname', 'commit_message'],
        ['date', 'repo_name', 'repo_slug', 'commit_type', 'commit_hash', 'commit_date', 'commit_author_type', 'commit_author_raw', 'commit_user_uuid', 'commit_user_account_id', 'commit_user_nickname', 'commit_message']
    )


def get_bitbucket_repo_commits(bitbucket_workspace, bitbucket_user, bitbucket_token, repo_name, repo_slug):

    page = 1
    pagelen = 100
    number_of_results = 0
    first_call = True
    next_page = False
    repo_commits_list = []

    print('{} - INFO - Reading Bitbucket repo commits from Bitbucket Cloud API for repo slug {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), repo_slug))

    while first_call == True or next_page == True:

        retry_for_api_ready = True
        retry_count = 0
        while retry_for_api_ready and retry_count<10:
            http_response = requests.get(
                'https://api.bitbucket.org/2.0/repositories/{}/{}/commits?pagelen={}&page={}'.format(bitbucket_workspace, repo_slug, str(pagelen), str(page)),
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
                http_response_item_author = http_response_item.get('author')

                if not http_response_item_author.get('user'):
                    commit_user_uuid = ""
                    commit_user_account_id = ""
                    commit_user_nickname = ""
                else:
                    commit_user_uuid = http_response_item_author['user']['uuid']
                    commit_user_account_id = http_response_item_author['user']['account_id']
                    commit_user_nickname = http_response_item_author['user']['nickname']

                commit_message = str(http_response_item.get('message')).replace('\n', '').replace('\r', '').replace('\t', ' ').replace('\f', '').replace('"','')
                if len(commit_message)>150:
                    commit_message = commit_message[:150] + '...'


                repo_commits_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'repo_name': repo_name,
                    'repo_slug': repo_slug,
                    'commit_type': http_response_item.get('type'),
                    'commit_hash': http_response_item.get('hash'),
                    'commit_date': http_response_item.get('date'),
                    'commit_author_type': http_response_item_author.get('type'),
                    'commit_author_raw': http_response_item_author.get('raw'),
                    'commit_user_uuid': commit_user_uuid,
                    'commit_user_account_id': commit_user_account_id,
                    'commit_user_nickname': commit_user_nickname,
                    'commit_message': commit_message
                })

                number_of_results = number_of_results + 1

            if "next" in http_response.json():
                next_page = True
            else:
                next_page = False
            page = page + 1
        else:
            next_page = False
            print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

        first_call = False

    print('{} - INFO - Reading Bitbucket repo commits from Bitbucket Cloud API for repo slug {}: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), repo_slug, number_of_results))

    return repo_commits_list


def export_all_bitbucket_repos_branches(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):

    repos_list = get_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token)

    repos_branches_list = []

    print('{} - INFO - Reading Bitbucket repos commits from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    for repo in repos_list:
        repo_branches_list = get_bitbucket_repo_branches(bitbucket_workspace, bitbucket_user, bitbucket_token, repo['repo_name'], repo['repo_slug'])
        repos_branches_list.extend(repo_branches_list)

    export_csv(
        export_filename,
        repos_branches_list,
        ['date', 'repo_name', 'repo_slug', 'ref_name', 'ref_type'],
        ['date', 'repo_name', 'repo_slug', 'ref_name', 'ref_type']
    )


def get_bitbucket_repo_branches(bitbucket_workspace, bitbucket_user, bitbucket_token, repo_name, repo_slug):

    page = 1
    pagelen = 50
    number_of_results = 0
    first_call = True
    next_page = False
    next_page_url = ''
    repo_branches_list = []

    print('{} - INFO - Reading Bitbucket repo branches from Bitbucket Cloud API for repo slug {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), repo_slug))

    while first_call == True or next_page == True:

        retry_for_api_ready = True
        retry_count = 0
        while retry_for_api_ready and retry_count<10:
            if next_page_url == '':
                http_response = requests.get(
                    'https://api.bitbucket.org/2.0/repositories/{}/{}/refs?pagelen={}'.format(bitbucket_workspace, repo_slug, str(pagelen)),
                    auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
                )
            else:
                http_response = requests.get(
                    '{}'.format(next_page_url),
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
                repo_branches_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'repo_name': repo_name,
                    'repo_slug': repo_slug,
                    'ref_name': http_response_item.get('name'),
                    'ref_type': http_response_item.get('type')
                })

                number_of_results = number_of_results + 1

            if "next" in http_response.json():
                next_page = True
                next_page_url = http_response.json().get('next')
            else:
                next_page = False
                next_page_url = ''
            page = page + 1
        else:
            next_page = False
            next_page_url = ''
            print('{} - WARN - http response: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), http_response.status_code))

        first_call = False

    print('{} - INFO - Reading Bitbucket repo branches from Bitbucket Cloud API for repo slug {}: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), repo_slug, number_of_results))

    return repo_branches_list


def git_clone_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token):

    repos_list = get_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token)

    print('{} - INFO - Git clone Bitbucket repos...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))

    for repo in repos_list:
        git_clone_command = 'git clone https://{}:{}@bitbucket.org/{}/{}.git git-clone/{}'.format(bitbucket_user, bitbucket_token, bitbucket_workspace, repo['repo_slug'], repo['repo_slug'])
        print('{} - INFO - git clone Bitbucket repo {}...'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), repo['repo_slug']))
        os.system(git_clone_command)
