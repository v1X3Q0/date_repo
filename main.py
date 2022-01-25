import re
import git
import os
import argparse
import xml.parsers.expat
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--date", "-d", required=True,
    help="date in the unix format YYYY-MM-DD")
parser.add_argument("--gitrepo", "-g",
    help="target git repo to date")
parser.add_argument("--repman", "-m",
    help="address of a repo manifest that will serve as the base")
parser.add_argument("--branch", "-b", required=True,
    help="target branch to carbon date")
parser.add_argument("--repopath",
    help="path for the repo")
parser.add_argument("--url", "-u", required=True
    help="url provided")

args = parser.parse_args()

def date_git(gitrepo_path, targdate):
    g = git.Git(gitrepo_path)

    # don't technically need it, but the following line gets the date
    # g.log("--before=\"{}\"".format(targdate), "-n", "1", "--format=%ci")
    
    commitstr = g.log("--before=\"{}\"".format(targdate), "-n", "1", "--format=%H")
    g.checkout("{}".format(commitstr))

def main():
    repopath = os.path.curdir

    if (args.repman != None) and (args.gitrepo != None):
        print("only a git repo or a repo manifest required")

    if args.repopath:
        os.makedirs(args.repopath)
        repopath = args.repopath
        os.chdir(repopath)      
    
    if args.repman != None:
        repo = git.Repo.clone_from("{}/{}".format(args.url, args.repman), repopath, branch=args.branch)
        date_git(args.repman, args.date)
        f = open("default.xml", "r")
        default_str = f.read()
        f.close()
        default_xml = ET.fromstring(default_str)
        for i in default_xml.getchildren():
            assignpath = i.get("path")
            # if it has a path, then it will exists in the repository
            if assignpath != None:
                os.makedirs(assignpath)
                repo = git.Repo.clone_from("{}/{}".format(args.url, i.get("name")),
                    assignpath, branch=i.get("revision"))
                os.chdir(assignpath)
                date_git(os.path.curdir, args.date)
                os.chdir(repopath)

    targdate = args.date

if __name__ == "__main__":
    main()