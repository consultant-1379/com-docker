#!/usr/bin/env python

import argparse
import sys
import subprocess
import traceback
import wget
import os

parser = argparse.ArgumentParser(description='Options for ansible')

mandatoryArgs = parser.add_argument_group('Mandatory arguments')
mandatoryArgs.add_argument('--hosts-file-url', action="store", dest="fileUrl", default=False, required=True)
args = parser.parse_args()

# Get the latest host information from repository
out = "/root/.ansible/hosts"

try:
    if os.path.isfile(out):
        print "Removing old hosts file"
        os.remove(out)

    print "Downloading hosts file from Gerrit"
    wget.download(args.fileUrl, out)
except:
    traceback.print_exc(file=sys.stdout)
    raise

# Run the ansible playbook which will run containers to update mirrors
playbook = "/mirror-playbook.yml"
vaultPassword = "/root/.vault_pass"
ansibleCommand = ["ansible-playbook", "-i", out, "--vault-password-file", vaultPassword, playbook]

try:
    print "Running playbook: " + playbook
    subprocess.check_call(ansibleCommand, stderr=subprocess.STDOUT)
except:
    traceback.print_exc(file=sys.stdout)
    raise
