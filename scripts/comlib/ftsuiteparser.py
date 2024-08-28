#!/usr/bin/env python

'''
This class parses the ft-suites.bash that COM's build scripts generates

'''
class FtSuiteParser:

    def __init__(self):
        self.options = {}

    def parse(self,filename):
        f = open(filename)

        for line in f:
            key,value = line.split("='")

            key = key.replace("run_ft_","")
            value = value.replace("'\n","")

            suiteFile,suiteName = value.split(" ")

            self.options[key.lower()] = [suiteFile.strip(), suiteName.strip()]


    def getName(self,suite):
        return self.options[suite][1]

    def getSuiteFile(self,suite):
        return self.options[suite][0]
