from buildbase import BuildBase
from cirpa.utils.shellhelper import execute, call
from cirpa.utils.git import Git

import shutil
import os
from os.path import join
import yaml
import glob
import sys

class BuildCbaComCodeChecker(BuildBase):

    def _build(self):

        cmakeConfig = self._args.buildtype

        # read the configuration file
        with open("/usr/src/scripts/buildscripts/cmake_config.yaml", 'r') as input:
            cfg = yaml.load(input)

        # setup the build dir
        execute(["mkdir", "-p", self._args.builddir])

        os.chdir(self._args.builddir)

        # add cmake options from the configuration file
        for key, value in cfg[cmakeConfig].items():
            self._cmakeOptions.add(key, value)

        # run cmake and make using codechecker
        returnValue = call(["CodeChecker", "log", "--output", "/compile_commands.json", "--build", "cmake " + " ".join(self._cmakeOptions.generate()) + " " + self._repoDir + " && " + "make -j" + self._args.makeWorkers + " " + "all" ], debug=True)
        if returnValue > 0:
            return returnValue

        git = Git()
        commitHash = git.getCommitHash(self._repoDir)
        if self._args.baseCode:
            returnValue = call(["/usr/src/scripts/buildscripts/code_checker/scripts/parse.sh", "COM", self._args.username, self._args.password, self._repoDir, commitHash, self._args.baseCode], debug=True)
        else:
            returnValue = call(["/usr/src/scripts/buildscripts/code_checker/scripts/parse.sh", "COM", self._args.username, self._args.password, self._repoDir, commitHash], debug=True)
        if returnValue > 0:
            print ("Error: CodeChecker analysis failed or new bugs are introduced.")
        return returnValue
