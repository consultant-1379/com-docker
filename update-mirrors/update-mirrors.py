#!/usr/bin/env python

import argparse
import os
import subprocess
import traceback
import sys

parser = argparse.ArgumentParser(description='Options for mirror update')

parser.add_argument('--vault-pass', action="store", dest="vaultPass", required=False)
parser.add_argument('--repo', action="store", dest="repo", nargs="+", required=True)
args = parser.parse_args()

identityFile = os.environ.get("IDENTITY")
decryptCommand = ["ansible-vault", "decrypt", identityFile, "--vault-password-file", args.vaultPass]

try:
    print "Decrypting the identity file"
    subprocess.check_call(decryptCommand, stderr=subprocess.STDOUT)
except:
    traceback.print_exc(file=sys.stdout)
    raise

gerritUrl = "gerritmirror.rnd.ki.sw.ericsson.se"
gerritUser = "cbacomci"
gerritRepo = "com-ansible"
mirrorPath= "/mirrors/"

# Create the url for cloning
gerritSshUrl = "ssh://" + gerritUser + "@" + gerritUrl + ":29418/"

umask = ['-c', 'core.sharedRepository=group']

for repo in args.repo:
    destination = mirrorPath + repo
    if "CBA/" in repo:
        destination = destination.replace("CBA/", "")

    destination += ".git"

    source = gerritSshUrl + repo

    try:
        if not os.path.isdir(destination):

            # Create the clone command
            gitCommand = ["git"] + umask + ["clone", "--mirror", source, destination]

            print "Cloning repository to: " + destination
            subprocess.check_call(gitCommand, stderr=subprocess.STDOUT)
        else:
            gitCommand = ["git", "-C", destination, "remote", "set-url", "origin", source]

            print "Updating the repository: " + destination
            subprocess.check_call(gitCommand, stderr=subprocess.STDOUT)

            gitCommand = ["git", "-C", destination, "remote", "update"]
            subprocess.check_call(gitCommand, stderr=subprocess.STDOUT)
    except:
        traceback.print_exc(file=sys.stdout)
        raise
