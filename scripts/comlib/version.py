import os
import re
import fnmatch
import sys

def getVersion(directoryPath):

    for file in os.listdir(directoryPath):
        if fnmatch.fnmatch(file, '*-runtime*'):
            runtimePackage = file

    # this regular expression is used for fetching version of format "1.0.0-1"
    matcher=re.search( r'^[a-zA-Z0-9_]+-([0-9]+.[0-9]+.[0-9]+-[0-9]+).*-runtime.*', runtimePackage, re.M)
    if matcher:
        version=matcher.group(1)

    # this regular expression is used for fetching version of format "R1A"
    matcher=re.search( r'^[a-zA-Z0-9_]+.*-runtime.*_([0-9a-zA-Z]*).tar.gz', runtimePackage, re.M)
    if matcher:
        version=matcher.group(1)

    return version
