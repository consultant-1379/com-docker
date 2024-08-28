from buildbase import BuildBase
from cirpa.utils.shellhelper import call
import os


class UpdateMvnRepository(BuildBase):

    def build(self):

        # setup the build dir

        os.chdir(self._repoDir + "/test/")

        command = ["mvn", "-v"]
        call(command)

        command = ["mvn", "-B", "-X", "compile"]
        call(command)
        return 0
