import os
import sys
import datetime

from util.config import (get_atlassian_config_file, get_bitbucket_config_file, get_cli_params)
from jira.users import (export_all_jira_groups, export_all_jira_groups_members, export_all_jira_users)
from jira.jira import (export_all_jira_projects)
from jira.confluence import (export_all_confluence_spaces)
from bitbucket.users import (export_all_bitbucket_users, export_all_bitbucket_groups_and_members)
from bitbucket.workspace import (export_all_bitbucket_projects, export_all_bitbucket_repos, export_all_bitbucket_repos_commits, export_all_bitbucket_repos_branches, git_clone_all_bitbucket_repos)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Get command line parameters
    config_file, action = get_cli_params(sys.argv[1:])

    # Create the export and/or config directories if doesnt exists
    export_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/export/"
    config_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/config/"
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    if not os.path.exists(export_path):
        os.makedirs(export_path)
        print("{} - INFO - The directory ""{}"" has been created".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), export_path))
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        print("{} - INFO - The directory ""{}"" has been created".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), config_path))

    # Execute the action requested
    if action == "export_all_jira_groups_and_members":
        atlassian_site, atlassian_user, atlassian_token = get_atlassian_config_file(config_path + config_file)
        groups_list = export_all_jira_groups(atlassian_site, atlassian_user, atlassian_token, export_path + "{}-atlassian-groups-{}.csv".format(current_date, atlassian_site))
        export_all_jira_groups_members(atlassian_site, atlassian_user, atlassian_token, groups_list, export_path + "{}-atlassian-groups-members-{}.csv".format(current_date, atlassian_site))

    elif action == "export_all_jira_users":
        atlassian_site, atlassian_user, atlassian_token = get_atlassian_config_file(config_path + config_file)
        export_all_jira_users(atlassian_site, atlassian_user, atlassian_token, export_path + "{}-atlassian-users-{}.csv".format(current_date, atlassian_site))

    elif action == "export_all_jira_projects":
        atlassian_site, atlassian_user, atlassian_token = get_atlassian_config_file(config_path + config_file)
        export_all_jira_projects(atlassian_site, atlassian_user, atlassian_token, export_path + "{}-jira-projects-{}.csv".format(current_date, atlassian_site))

    elif action == "export_all_confluence_spaces":
        atlassian_site, atlassian_user, atlassian_token = get_atlassian_config_file(config_path + config_file)
        export_all_confluence_spaces(atlassian_site, atlassian_user, atlassian_token, export_path + "{}-confluence-spaces-{}.csv".format(current_date, atlassian_site))

    elif action == "export_all_bitbucket_users":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_users(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-users-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "export_all_bitbucket_groups_and_members":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_groups_and_members(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-groups-{}.csv".format(current_date, bitbucket_workspace), export_path + "{}-bitbucket-groups-members-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "export_all_bitbucket_projects":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_projects(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-projects-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "export_all_bitbucket_repos":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-repos-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "export_all_bitbucket_repos_commits":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_repos_commits(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-commits-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "export_all_bitbucket_repos_branches":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        export_all_bitbucket_repos_branches(bitbucket_workspace, bitbucket_user, bitbucket_token, export_path + "{}-bitbucket-branches-{}.csv".format(current_date, bitbucket_workspace))

    elif action == "git_clone_all_bitbucket_repos":
        bitbucket_workspace, bitbucket_user, bitbucket_token = get_bitbucket_config_file(config_path + config_file)
        git_clone_all_bitbucket_repos(bitbucket_workspace, bitbucket_user, bitbucket_token)
