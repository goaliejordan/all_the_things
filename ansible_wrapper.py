## perform <command> --repo <repo_name> --tag <tag> [ --env <environment> ]
## Output the logging
#where <command> maps to a playbook (release.yml)
#repo is just a name (`rio` would map to `deployments/repo.git`)
#and tag is the tag within the repo to deploy (a branch, tag, hash, whatever)
import argparse
import logging
import os
import subprocess
import re

join = os.path.join

# rorepo is a a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with
repo = Repo(self.rorepo.working_tree_dir)
assert not repo.bare

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def gitBranch(repo, tag):
    subprocess.call(["git", "clone", "-b", "tag", "repo"])
    ## How to handle user login?
    dir = re.match('[^\/]+$', repo)
    os.chdir(dir)

def main():
    hosts_dir_root = "/opt/connexity/ansible/"
    hitw_deploy_user = "hitwdeployer"
    ansible_argument = [
            "ansible-playbook",
            "{}.yml".format(args.action),
            "-i",
            "hosts_dir_root{}".format(args.environment),
            "-i",
            "./hosts",
            "-u",
            "{}".format(hitw_deploy_user)
    ]

    parser = argparse.ArgumentParser(description='Deploy from ansible-playbook')
    parser.add_argument('action',
                        help='action to perform: release, start, stop, etc')
    parser.add_argument('--repo',
                        help='name of repo that contains the deploy branch')
    parser.add_argument('--tag',
                        help='name/tag/hash of branch containing deploy files')
    parser.add_argument('--env',
                        help='environment to deploy to. prod/dev/stage')
    parser.add_argument('--dryrun',
                        help='Outputs ansible-playbook results without run')
    args = parser.parse_args()

    ansible_argument = [
        "ansible-playbook",
        "{}.yml".format(args.action),
        "-i",
        "hosts_dir_root{}".format(args.environment),
        "-i",
        "./hosts",
        "-u",
        "{}".format(hitw_deploy_user)
    ]

    if args.dryrun:
        ansible_argument.append("-C")


exit(
        main()
)
