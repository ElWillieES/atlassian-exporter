import datetime
import requests
from requests.auth import HTTPBasicAuth
from util.export import (export_csv)


def export_all_bitbucket_projects(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):
    page = 1
    pagelen = 50
    number_of_results = 0
    first_call = True
    projects_list = []

    print('{} - INFO - Reading Bitbucket projects from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or next_page == True:
        projects_response = requests.get(
            'https://api.bitbucket.org/2.0/workspaces/{}/projects?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
            auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
        ).json()

        number_of_results = projects_response['size']
        for project in projects_response['values']:
            projects_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'project_key': project['key'],
                'project_uuid': project['uuid'],
                'project_name': project['name'],
                'is_private': project['is_private'],
                'description': project['description'],
                'created_on': project['created_on'],
                'updated_on': project['updated_on'],
                'has_publicly_visible_repos': project['has_publicly_visible_repos']
            })
        if "next" in projects_response:
            next_page = True
        else:
            next_page = False
        page = page + 1
        first_call = False

    print('{} - INFO - Total projects: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    export_csv(
        export_filename,
        projects_list,
        ['date', 'project_key', 'project_uuid', 'project_name', 'is_private', 'description', 'created_on', 'updated_on', 'has_publicly_visible_repos'],
        ['date', 'project_key', 'project_uuid', 'project_name', 'is_private', 'description', 'created_on', 'updated_on', 'has_publicly_visible_repos']
    )


def export_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token, export_filename):
    page = 1
    pagelen = 50
    number_of_results = 0
    first_call = True
    repos_list = []

    print('{} - INFO - Reading Bitbucket repos from Bitbucket Cloud API'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")))
    while first_call == True or next_page == True:
        repos_response = requests.get(
            'https://api.bitbucket.org/2.0/repositories/{}/?page={}&pagelen={}'.format(bitbucket_workspace, str(page), str(pagelen)),
            auth=HTTPBasicAuth(bitbucket_user, bitbucket_token)
        ).json()

        number_of_results = repos_response['size']
        for repo in repos_response['values']:
            repos_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'project_key': repo['project']['key'],
                'project_uuid': repo['project']['uuid'],
                'project_name': repo['project']['name'],
                'repo_name': repo['name'],
                'repo_slug': repo['slug'],
                'description': repo['description'],
                'is_private': repo['is_private'],
                'fork_policy': repo['fork_policy'],
                'created_on': repo['created_on'],
                'updated_on': repo['updated_on'],
                'size': repo['size'],
                'has_issues': repo['has_issues'],
                'has_wiki': repo['has_wiki'],
                'uuid': repo['uuid']
            })
        if "next" in repos_response:
            next_page = True
        else:
            next_page = False
        page = page + 1
        first_call = False

    print('{} - INFO - Total repos: {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(number_of_results)))

    export_csv(
        export_filename,
        repos_list,
        ['date', 'project_key', 'project_uuid', 'project_name', 'repo_name', 'repo_slug', 'description', 'is_private', 'fork_policy', 'created_on', 'updated_on', 'size', 'has_issues', 'has_wiki', 'uuid'],
        ['date', 'project_key', 'project_uuid', 'project_name', 'repo_name', 'repo_slug', 'description', 'is_private', 'fork_policy', 'created_on', 'updated_on', 'size', 'has_issues', 'has_wiki', 'uuid']
    )
