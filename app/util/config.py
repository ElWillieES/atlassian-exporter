import datetime
import json
import sys, getopt
import os


def show_help():
    print("atlassian-exporter is a free and open source tool intended to export some Atlassian Cloud and Bitbucket Cloud data,")
    print("like users, groups, groups membership, projects, and so on.")
    print()
    print("Usage: atlassian-exporter.py -c <configfile> -a <action>")
    print()
    print("Mandatory arguments to long options are mandatory for short options too.")
    print("  -h, --help           Display this help and exit")
    print("  -c, --configfile     Atlassian config file or Bitbucket config file, depending on the action selected")
    print("                       configFile must be located in the ./config directory")
    print("  -a, --action         Action to be executed. Exported data will be located in the ./export directory")
    print("                       The action selected must be one of the following:")
    print()
    print("                       export_all_jira_groups_and_members")
    print("                       export_all_jira_users")
    print("                       export_all_jira_projects")
    print("                       export_all_confluence_spaces")
    print("                       export_all_bitbucket_users")
    print("                       export_all_bitbucket_groups_and_members")
    print("                       export_all_bitbucket_projects")
    print("                       export_all_bitbucket_repos")
    print("                       export_all_bitbucket_repos_commits")
    print("                       export_all_bitbucket_repos_branches")
    print("                       git_clone_all_bitbucket_repos")
    print()
    print("Examples:")
    print("atlassian-exporter.py -c atlassian_conn_mysite.json -a export_all_jira_groups_and_members")
    print("atlassian-exporter.py --configfile atlassian_conn_mysite.json --action export_all_jira_projects")
    print("atlassian-exporter.py --configfile=bitbucket_conn_myworkspace.json --action=export_all_bitbucket_projects")
    print()
    print("More info at: https://github.com/ElWillieES/atlassian-exporter")
    print()


def get_cli_params(cli_args):
    config_file = ""
    action = ""

    try:
        opts, args = getopt.getopt(cli_args, "hc:a:", ["help", "configfile=", "action="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-c", "--configfile"):
            config_file = arg
        elif opt in ("-a", "--action"):
            action = arg

    if action != "" and action not in ("export_all_jira_groups_and_members", "export_all_jira_users", "export_all_jira_projects", "export_all_confluence_spaces", "export_all_bitbucket_users", "export_all_bitbucket_groups_and_members", "export_all_bitbucket_projects", "export_all_bitbucket_repos", "export_all_bitbucket_repos_commits", "export_all_bitbucket_repos_branches", "git_clone_all_bitbucket_repos"):
        print("The action specified as parameter, is not valid.")
        print()
        action = ""

    if config_file == "" or action == "":
        show_help()
        sys.exit(2)

    return config_file, action

def get_config_file(config_filename):
    print("{} - INFO - Reading config file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), config_filename))
    config = {}
    try:
        file = open(config_filename)
        config = json.load(file)
        file.close()
        return config
    except Exception as e:
        print("{} - ERROR - Error reading file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), e))
        exit()

def get_atlassian_config_file(config_filename):

    config_atlassian_conn = get_config_file(config_filename)
    atlassian_site = config_atlassian_conn["atlassian-site"]
    atlassian_user = config_atlassian_conn["atlassian-user"]
    atlassian_token = config_atlassian_conn["atlassian-token"]

    return atlassian_site, atlassian_user, atlassian_token


def get_bitbucket_config_file(config_filename):

    config_bitbucket_conn = get_config_file(config_filename)
    bitbucket_workspace = config_bitbucket_conn["bitbucket-workspace"]
    bitbucket_user = config_bitbucket_conn["bitbucket-user"]
    bitbucket_token = config_bitbucket_conn["bitbucket-token"]

    return bitbucket_workspace, bitbucket_user, bitbucket_token

