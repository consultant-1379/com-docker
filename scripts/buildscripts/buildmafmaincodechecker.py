from buildbase import BuildBase

from cirpa.utils.shellhelper import execute, call
from cirpa.utils.git import Git

import os
from os.path import join
import yaml
import tarfile
import urllib2
import base64
import shutil
import time


class BuildMafMainCodeChecker(BuildBase):

    """
    Helper function to download packages
    from artifactoty
    """
    # TODO: Move this funtion to a common location
    def download_file(self,url):
         file_name = url.split('/')[-1]
         USER = os.getenv('ADMIN_USER')
         PASSWORD = os.getenv('ADMIN_PASSWORD')
         print ("Downloading the file: " + file_name)
         request = urllib2.Request(url)
         b64auth = base64.standard_b64encode("%s:%s" % (USER,PASSWORD))
         request.add_header("Authorization", "Basic %s" % b64auth)
         ulib = urllib2.urlopen(request)

         file_obj = open(file_name, 'wb')

         file_size_dl = 0
         block_sz = 8192
         while True:
             buffer = ulib.read(block_sz)
             if not buffer:
                 break

             file_size_dl += len(buffer)
             file_obj.write(buffer)

         file_obj.close()
         return file_name

    def _build(self):

        os.chdir("/")
        artifactory_prebuilt_url="https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-com-ci-local/pre-built/pre-built.tar.gz"
        downloaded_file=self.download_file(artifactory_prebuilt_url)

        #Extract the downloaded tar.gz file
        tar = tarfile.open(downloaded_file, "r:gz")
        tar.extractall()
        tar.close()

        cmakeConfig = self._args.buildtype

        # add $USER environmental variable to the system
        os.environ["USER"] = "root"

        # add $MAF_TRUNK environmental variable to the system
        os.environ["MAF_TRUNK"] = self._repoDir

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

        buildDir = os.path.join(self._repoDir, "build")
        # run cmake and make using codechecker
        returnValue = call(["CodeChecker", "log", "--output", "/compile_commands.json", "--build", "cmake " + " ".join(self._cmakeOptions.generate()) + " " + buildDir+ " && " + "make -j" + self._args.makeWorkers + " " + "all" ], debug=True)
        if returnValue > 0:
            return returnValue

        git = Git()
        commitHash = git.getCommitHash(self._repoDir)

        if self._args.baseCode:
            returnValue = call(["/usr/src/scripts/buildscripts/code_checker/scripts/parse.sh", "MAF-MAIN", self._args.username, self._args.password, self._repoDir, commitHash, self._args.baseCode], debug=True)
        else:
            returnValue = call(["/usr/src/scripts/buildscripts/code_checker/scripts/parse.sh", "MAF-MAIN", self._args.username, self._args.password, self._repoDir, commitHash], debug=True)
        if returnValue > 0:
            print ("Error: CodeChecker analysis failed or new bugs are introduced.")
        return returnValue
