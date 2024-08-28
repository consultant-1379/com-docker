from buildbase import BuildBase
from cirpa.utils.shellhelper import execute, call
from cirpa.utils.createtar import createTar, normalizePath
from comlib.version import getVersion

import shutil
import os
from os.path import join
import yaml
import glob
import sys

class BuildCbaCom(BuildBase):

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

        # run cmake
        returnValue = call(["cmake"] + self._cmakeOptions.generate() + [self._repoDir], debug=True)

        if returnValue > 0:
            return returnValue  # cmake failed do not try to run make

        # run make
        makeCommand = ["make", "-j" + self._args.makeworkers]
        if self._args.useVerbose:
            makeCommand.append("VERBOSE=1")
        returnValue = call(makeCommand, debug=True)
        if returnValue > 0:
            return returnValue

        # copy com-${VERSION}-runtime.tar.gz
        comBuildDir = self._args.builddir
        comMainBuildDir = join(comBuildDir, "com-build")

        comVersion = self._args.comVersion
        if comVersion is None:
            comVersion = getVersion(join(comMainBuildDir, "dist"))

        fileslist = {"com-" + comVersion + "-runtime.tar.gz", "com_x86_64-*-runtime-*.tar.gz", "com-pt-test-*.noarch.rpm"}
        toFile = normalizePath(join(comBuildDir, "dist"))
        for f in fileslist:
            files = glob.glob(join(comMainBuildDir, "dist", f))
            for fromFile in files:
                print "found package: " + fromFile
                shutil.copy(fromFile, toFile)

        distPackagesPath = toFile
        runtimePackage = join(distPackagesPath, "com_x86_64-"+ comVersion + "-runtime-sle-cxp9028493.tar.gz")
        deploymentPackage = join(distPackagesPath, "com_x86_64-"+ comVersion +"-deployment-sle-cxp9028492.tar.gz")

        cptBinary = execute(['find', '/', '-name', 'cptlint'], debug=True)
        output = execute([cptBinary.strip(), '--package-type', 'runtime', runtimePackage], debug=True)
        if "ERROR" in output or "Failure" in output:
            print ("Runtime Package validation failed: {}".format(output))
            return 1
        output = execute([cptBinary.strip(), '--package-type', 'deployment', deploymentPackage], debug=True)
        if "ERROR" in output or "Failure" in output:
            print ("Deployment Package validation failed: {}".format(output))
            return 1

        # TODO revome this if not needed after implementation of cluster on docker
        # Workaround to install-remove test case from legacy jenkins
        # create com_build settings file
        comBuildFile = open("com_build.settings", "w")

        comBuildFile.write("export OLD_BUILD_DIR=" + comMainBuildDir + "\n")
        comBuildFile.write("export OLD_COM_DEPS_DIR=" + self._repoDir + "/dummy\n")
        comBuildFile.write("export BUILD_TARGET=native64\n")
        comBuildFile.write("export OLD_WORKSPACE=" + self._repoDir + "/com-main\n")

        comBuildFile.close()

        fromPath = self._args.builddir + "/com_build.settings"
        toPath = self._repoDir + "/com-main/com_build.settings"
        shutil.move(fromPath, toPath)

        # generate the com test package
        if returnValue == 0:
            # create the test tar
            self._createTestTar(self._repoDir, comVersion)

        return returnValue

    def _createTestTar(self, srcCom, comVersion):

        srcComMain = join(srcCom, "com-main")
        comsaSourceDir = join(self._srcDir, "comsa-source")
        comBuildDir = self._args.builddir
        comMainBuildDir = join(comBuildDir, "com-build")
        comsaVerificationDir = join(self._srcDir, "comsa-verification")

        if self._args.comsaTest == 'comsa':
            excludes = []

            includes = [
                comsaVerificationDir,
                comsaSourceDir
            ]
        else:
            # source excludes
            excludes = [
                join(srcCom, ".git"),
                join(srcCom, "comsa-source"),
                join(srcComMain, ".git"),
                join(srcComMain, "3pp", "src")
            ]

            # com-main build excludes
            excludes = excludes + [
                join(comMainBuildDir, "dist"),
                join(comMainBuildDir, "3pp"),
                join(comMainBuildDir, "bin"),
                join(comMainBuildDir, "tmp"),
                join(comMainBuildDir, "com_install"),
                join(comMainBuildDir, "CMakeFiles"),
                join(comMainBuildDir, "unittests"),  # removes ~520M of unittest binaries
            ]

            includes = [
                srcCom,
                comMainBuildDir
            ]

            # look for the PT rpm, CONFIGPKG spd's and add to tar file if found
            # com-pt-test-*-${COM_VERSION}.noarch.rpm
            comTestFiles = glob.glob(join(comMainBuildDir, "dist", "com-pt-test-*.noarch.rpm"))
            # CONFIGPKG_COM_R1-CXP9013822_3.sdp, CONFIGPKG_COM_R1_M-CXP9013822_3.sdp
            comTestFiles += glob.glob(join(comMainBuildDir, "dist", "CONFIGPKG_COM_*.sdp"))
            for n in comTestFiles:
                print "found PT rpm: " + n
                includes.append(n)

        filename = normalizePath(join(comBuildDir, "dist", "com-" + comVersion + "-test.tar.gz"))
        print "filename: " + filename

        createTar(filename, includes, excludes)
