#!/usr/bin/env python

import argparse
import sys
import subprocess
import traceback
import wget
import os
import ssl

parser = argparse.ArgumentParser(description='Options for ansible')

mandatoryArgs = parser.add_argument_group('Mandatory arguments')
mandatoryArgs.add_argument('--hosts-file-url', action="store", dest="fileUrl", required=True, help='Inventory File')
mandatoryArgs.add_argument('--start', action="store_true", help='Starts slave containers')
mandatoryArgs.add_argument('--stop', action="store_true", help='Stops slave containers')

optionalArgs = parser.add_argument_group('Optional arguments')
optionalArgs.add_argument('--hardware-type', action="store", dest="hardware", choices=['characteristics_lde_stc_135_sp5','characteristics_stc_137_sp5','high-load_lde_stc_136_sp5','high-load_stc_138_sp5'], help='Type of hardware')

args = parser.parse_args()

# Get the latest host information from repository
hostFile = "/inventories/hosts"

# Disable certificate verification
ssl._https_verify_certificates(enable=False)

#try:
#    if os.path.isfile(hostFile):
#        print("Removing old hosts file")
#        os.remove(hostFile)

#    print("Downloading hosts file from Gerrit")
#    wget.download(args.fileUrl, hostFile)
#except:
#    traceback.print_exc(file=sys.stdout)
#    raise

# Run the ansible playbook which will run containers attached to hardwares
playbook = "/slave-playbook.yml"
vaultPassword = "/root/.vault_pass"
if args.start:
    ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=start"]
elif args.stop:
    if not args.hardware:
        ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=stop"]
    elif args.hardware == 'characteristics_lde_stc_135_sp5':
        ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=stop-characteristics_lde_stc_135_sp5"]
    elif args.hardware == 'characteristics_stc_137_sp5':
        ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=stop-characteristics_stc_137_sp5"]
    elif args.hardware == 'high-load_lde_stc_136_sp5':
        ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=stop-high-load_lde_stc_136_sp5"]
    elif args.hardware == 'high-load_stc_138_sp5':
        ansibleCommand = ["ansible-playbook", "-i", hostFile, "--vault-password-file", vaultPassword, playbook, "--tags=stop-high-load_stc_138_sp5"]
try:
    print("Running playbook: " + playbook)
    subprocess.check_call(ansibleCommand, stderr=subprocess.STDOUT)
except:
    traceback.print_exc(file=sys.stdout)
    raise
