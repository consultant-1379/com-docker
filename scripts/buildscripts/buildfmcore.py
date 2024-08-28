from buildbase import BuildBase

from cirpa.utils.shellhelper import execute, call
from cirpa.utils.createtar import createTar, normalizePath
from comlib.version import getVersion

import shutil
import os
from os.path import join
import yaml


class BuildFmCore(BuildBase):

    def _build(self):
        cmakeConfig = self._args.buildtype

        # read the configuration file
        with open("/usr/src/scripts/buildscripts/cmake_config.yaml", 'r') as input:
            cfg = yaml.load(input)

        # setup the build dir
        command = ["mkdir", "-p", self._args.builddir]
        execute(command)

        os.chdir(self._args.builddir)

        # add cmake options from the configuration file
        for key, value in cfg[cmakeConfig].items():
            self._cmakeOptions.add(key, value)

        # run cmake
        returnValue = call(["cmake"] + self._cmakeOptions.generate() + [self._repoDir], debug=True)

        if returnValue > 0:
            return returnValue

        # run make
        returnValue = call(["make", "-j" + self._args.makeworkers, "all"], debug=True)
        if returnValue > 0:
            return returnValue

        returnValue = call(["make", "-j" + self._args.makeworkers, "release"], debug=True)
        if returnValue > 0:
            return returnValue

        returnValue = call(["make", "-j" + self._args.makeworkers, "build-ft"], debug=True)

        # TODO revome this if not needed after complete implementation of docker
        # Workaround to run test cases from legacy jenkins with build from dev jenkins
        # create com_build settings file
        comBuildFile = open("com_build.settings", "w")

        comBuildFile.write("export OLD_BUILD_DIR=" + self._args.builddir + "\n")
        buildTarget = self._cmakeOptions.generate()
        target = 'native64'
        comBuildFile.write("export OLD_COM_DEPS_DIR=" + self._repoDir + "/dummy\n")
        comBuildFile.write("export BUILD_TARGET=" + target + "\n")
        comBuildFile.write("export OLD_WORKSPACE=" + self._repoDir + "\n")

        comBuildFile.close()

        fromPath = self._args.builddir + "/com_build.settings"
        toPath = self._repoDir + "/com_build.settings"
        shutil.move(fromPath, toPath)

        fmcoreVersion = self._args.fmcoreVersion
        if fmcoreVersion is None:
            fmcoreVersion = getVersion(join(self._args.builddir, "dist"))
        # generate the fmcore test package
        if returnValue == 0:
            # create the test tar
            self._createTestTar(self._repoDir, fmcoreVersion)

        return returnValue

    def _createTestTar(self, srcFmCore, fmcoreVersion):

        fmCoreBuildDir = self._args.builddir

        # source excludes
        excludes = [
            join(srcFmCore, ".git"),
            join(srcFmCore, "3pp", "src")
        ]

        # fm-core build excludes
        excludes = excludes + [
            join(fmCoreBuildDir, "dist"),
            #TODO Uncomment these two lines when all the local FTs are ported to run in remote FT
            # join(comBuildDir, "3pp"),
            # join(comBuildDir, "bin"),
            join(fmCoreBuildDir, "tmp"),
            join(fmCoreBuildDir, "com_install"),
            join(fmCoreBuildDir, "CMakeFiles"),
            join(fmCoreBuildDir, "resources", "unittests"),  # removes ~520M of unittest binaries
        ]

        includes = [
            srcFmCore,
            fmCoreBuildDir
        ]

        filename = normalizePath(join(fmCoreBuildDir, "dist", "fmcore-" + fmcoreVersion + "-test.tar.gz"))
        print ("filename: {}".format(filename))

        createTar(filename, includes, excludes)
