from buildbase import BuildBase

from cirpa.utils.shellhelper import execute, call
from cirpa.utils.createtar import createTar, normalizePath
from comlib.version import getVersion

import shutil
import os
from os.path import join
import yaml


class BuildComMain(BuildBase):

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
        makeCommand = ["make", "-j" + self._args.makeworkers]
        if self._args.useVerbose:
            makeCommand.append("VERBOSE=1")
        buildOptions = ["all", "release", "build-ft"]
        for item in buildOptions:
            makeCommand.append(item)
            returnValue = call(makeCommand, debug=True)
            if returnValue > 0:
                return returnValue
            makeCommand.pop()

        # TODO revome this if not needed after complete implementation of docker
        # Workaround to run test cases from legacy jenkins with build from dev jenkins
        # create com_build settings file
        comBuildFile = open("com_build.settings", "w")

        comBuildFile.write("export OLD_BUILD_DIR=" + self._args.builddir + "\n")
        buildTarget = self._cmakeOptions.generate()
        target = 'native64'
        if any('LSB' in item for item in buildTarget):
            target = 'lsb-x86_64'
        comBuildFile.write("export OLD_COM_DEPS_DIR=" + self._repoDir + "/dummy\n")
        comBuildFile.write("export BUILD_TARGET=" + target + "\n")
        comBuildFile.write("export OLD_WORKSPACE=" + self._repoDir + "\n")

        comBuildFile.close()

        fromPath = self._args.builddir + "/com_build.settings"
        toPath = self._repoDir + "/com_build.settings"
        shutil.move(fromPath, toPath)

        comVersion = self._args.comVersion
        if comVersion is None:
            comVersion = getVersion(join(self._args.builddir, "dist"))

        # generate the com test package
        if returnValue == 0:
            # create the test tar
            self._createTestTar(self._repoDir, comVersion)

        return returnValue

    def _createTestTar(self, srcComMain, comVersion):

        comBuildDir = self._args.builddir

        # source excludes
        excludes = [
            join(srcComMain, ".git"),
            join(srcComMain, "3pp", "src")
        ]

        # com-main build excludes
        excludes = excludes + [
            join(comBuildDir, "dist"),
            #TODO Uncomment these two lines when all the local FTs are ported to run in remote FT
            # join(comBuildDir, "3pp"),
            # join(comBuildDir, "bin"),
            join(comBuildDir, "tmp"),
            join(comBuildDir, "com_install"),
            join(comBuildDir, "CMakeFiles"),
            join(comBuildDir, "resources", "unittests"),  # removes ~520M of unittest binaries
        ]

        includes = [
            srcComMain,
            comBuildDir
        ]

        # look for the PT rpm and add to tar file if found
        # com-pt-test-*-${COM_VERSION}.noarch.rpm
        import glob
        ptfiles = glob.glob(join(comBuildDir, "dist", "com-pt-test-*.noarch.rpm"))
        for n in ptfiles:
            print "found PT rpm: " + n
            includes.append(n)

        filename = normalizePath(join(comBuildDir, "dist", "com-" + comVersion + "-test.tar.gz"))
        print "filename: " + filename

        createTar(filename, includes, excludes)
