import re
import git
import os
import argparse
from subprocess import PIPE
from subprocess import Popen
import xml.parsers.expat
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--date", "-d", required=True,
    help="date in the unix format YYYY-MM-DD")
parser.add_argument("--url", "-u",
    help="url provided")
parser.add_argument("--gitrepo", "-g",
    help="target git repo to date")
parser.add_argument("--repman", "-m",
    help="repo manifest url suffix that will serve as the base")
parser.add_argument("--branch", "-b",
    help="target branch to carbon date")
parser.add_argument("--repopath",
    help="path to use as the base for the repo, if not specified will use curdir")

args = parser.parse_args()

def date_git(gitrepo_path, targdate):
    g = git.Git(gitrepo_path)

    commitstr = g.log("--before=\"{}\"".format(targdate), "-n", "1", "--format=%H")
    if commitstr == "":
        commitdate = g.log("-n", "1", "--format=%ci")
        print("WARNING: no commit for repo {} before {}, earliest {}".format(gitrepo_path, targdate, commitdate))
        return
    
    # don't technically need it, but the following line gets the date
    commitdate = g.log("--before=\"{}\"".format(targdate), "-n", "1", "--format=%ci")
    
    print("repo {} checking out commit {} dated {}".format(gitrepo_path, commitstr, commitdate))
    g.checkout("{}".format(commitstr))

def update_git(urlbase, assignpath, reponame, repobranch, targdate):
    cwd = os.path.abspath(os.path.curdir)
    if os.path.exists(assignpath) == False:
        os.makedirs(assignpath)
        repo = git.Repo.clone_from("{}/{}".format(urlbase, reponame),
            assignpath, branch=repobranch)
    # os.chdir(assignpath)
    # date_git(os.path.curdir, targdate)
    date_git(assignpath, targdate)
    os.chdir(cwd)

def sync_date(urlbase, repomanifest, repopath, repobranch, targdate):
    proc = Popen(["repo", "manifest"], stdout=PIPE)
    default_str = proc.stdout.read()
    try:
        default_str = default_str.decode("utf-8")
        default_xml = ET.fromstring(default_str)
    except:
        repo = git.Repo.clone_from("{}/{}".format(urlbase, repomanifest), repopath, branch=repobranch)
        date_git(repomanifest, targdate)
        f = open("default.xml", "r")
        default_str = f.read()
        f.close()
        default_xml = ET.fromstring(default_str)

    for i in default_xml.getchildren():
        assignpath = i.get("path")
        # if it has a path, then it will exists in the repository
        if assignpath != None:
            update_git(urlbase, assignpath, i.get("name"), i.get("revision"), targdate)

def main():
    repopath = os.path.abspath(os.path.curdir)

    # can't have a repo manifest and a git repo to update
    if (args.repman != None) and (args.gitrepo != None):
        print("only a git repo or a repo manifest required")

    # if the repo output path doesn't exists, we will be pulling it.
    if args.repopath != None:
        if os.path.exists(args.repopath) == False:
            os.makedirs(args.repopath)
            repopath = args.repopath
            os.chdir(repopath)
    
    if args.gitrepo != None:
        update_git(args.url, args.gitrepo, args.gitrepo, args.branch)
    else:
        sync_date(args.url, args.repman, args.repopath, args.branch, args.date)

if __name__ == "__main__":
    main()