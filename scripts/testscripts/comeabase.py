import os
import sys

from cirpa.utils.shellhelper import execute
from cirpa.utils.git import Git
from comlib.commetafile import ComMetaFile


class ComEABase:

    def __init__(self, args):
        workDir = os.getcwd()
        if args.localsrc:
            print "**************** building from local repo **************"
            srcDir = "/"
            repoDir = args.localsrc
        else:
            srcDir = os.path.join(workDir, "src")
            repoDir = os.path.join(srcDir, args.repo)

        self._repoDir = repoDir
        self._srcDir = srcDir
        self._args = args
        self._gitPath = os.path.join(self._repoDir, ".git")

    # this function should not be overriden, please override _build and _clone function instead
    def build(self):
        self._clone()
        return self._build()

    def _build(self):
        raise NotImplementedError

    def _clone(self):
        git = Git()
        if not self._args.localsrc:
            # not a local build, clone the repo
            execute(["mkdir", "-p", self._srcDir])

            os.chdir(self._srcDir)

            project = None
            if self._args.gerritProject:
                project = os.path.basename(self._args.gerritProject)

            if (self._args.commit.startswith("refs/changes") and project and project != self._args.repo):
                git.clone(self._args.branch, self._args.repo, self._args.mirrorpath, self._srcDir)
            else:
                git.clone(self._args.commit, self._args.repo, self._args.mirrorpath, self._srcDir)

        # check if build triggered by gerrit
        if self._args.gerritTrigger:
            if self._args.gerritTrigger == 'trigger':
                self._update_submodule(git)

        # always create the build meta file
        commitHash = git.getCommitHash(self._repoDir)
        repoUrl = git.getRepoUrl(self._repoDir)
        filepath = os.path.join(self._args.builddir, "dist")

        self._createMetaFile(filepath, repoUrl, commitHash)

    def _createMetaFile(self, metaLocation, repoUrl, commitHash):
        filename = "com.meta.info"

        print execute(["mkdir", "-p", metaLocation])

        meta = ComMetaFile()

        if os.path.isfile("/" + filename):
            meta.load("/" + filename)

        meta.addBuildInfo(repoUrl, commitHash)

        meta.write(os.path.join(metaLocation, filename))

    def _update_submodule(self, git):

        # fetch gerrit project name and path
        projectDetails = git.get_submodule_detail(self._gitPath, self._args.gerritProject, self._repoDir)
        if projectDetails is None:
            print("Error: Gerrit project is not a submodule !")
            sys.exit(1)

        projectPath = projectDetails[1]
        print(projectPath)

        # Exit and do nothing if the commit is already a parent of submodule HEAD pointer
        git.check_submodule_head(projectPath, self._args.patchset)

        # Get the url of the project's origin
        projectOriginUrl = git.get_project_url(projectPath)

        # Fetch and checkout the triggering patch set
        git.checkout_patchset(projectPath, projectOriginUrl, self._args.commit)

        # Update submodules to get latest changes of submodule of the project
        git.update_submodule(projectPath)
