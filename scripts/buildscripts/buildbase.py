import os
import traceback
import sys
import subprocess

from cirpa.utils.shellhelper import execute
from cirpa.utils.git import Git
from comlib.commetafile import ComMetaFile


class BuildBase:

    def __init__(self, args, cmakeOptions):
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
        self._cmakeOptions = cmakeOptions
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

            if self._args.comsaTest == 'comsa':
                git.clone("comsa_dev", "comsa-source", self._args.mirrorpath, self._srcDir)
                git.clone("merge_com", "comsa-verification", self._args.mirrorpath, self._srcDir)

        # check if build triggered by gerrit
        if self._args.gerritTrigger:
            if self._args.gerritTrigger == 'trigger':
                self._update_submodule(git)
            else:
                self._update_umbrella_repo(git)

        # checkout maf master branch if latest maf flag
        if self._args.mafLatest:
            returnPathFlag = True
            moduleName = "maf-main"
            mafDir = (git.get_submodule_detail(self._gitPath, moduleName, self._repoDir))[1]
            mafBranch = "master"
            print ("Checking out maf master branch")
            git.checkout_branch(mafDir, mafBranch)

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
            print("Gerrit project is not a submodule !")
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

    def _update_umbrella_repo(self, git):

        # decrypt vault password
        identityFile = os.environ.get("IDENTITY")
        decryptCommand = ["ansible-vault", "decrypt", identityFile, "--vault-password-file", self._args.vaultPass]

        try:
            print "Decrypting the identity file"
            subprocess.check_call(decryptCommand, stderr=subprocess.STDOUT)
        except:
            traceback.print_exc(file=sys.stdout)
            raise

        # Clean repository if it is dirty
        git.clean_dirty_repository(self._repoDir)

        # fetch gerrit project path
        projectName = os.path.basename(self._args.gerritProject)
        projectPath = os.path.join(self._repoDir, projectName)

        # Exit and do nothing if the commit is already a parent of submodule HEAD pointer
        git.check_submodule_head(projectPath, self._args.patchset)

        # fetch and checkout gerrit branch
        checkout_target = "origin/" + self._args.gerritBranch
        git.checkout_branch(projectPath, checkout_target)

        # check if any update is needed
        if git.is_repository_dirty(self._repoDir) > 0:
            print("No changes in the submodule %s found" % projectName)
            sys.exit(1)

        # set user for commit
        userEmail = "\"PDLCOMCICO@pdl.internal.ericsson.com\""
        userName = "\"CBA COM CI user\""

        git.set_comci_user(self._repoDir, userEmail, userName)

        # Add updated submodule to umbrella repo
        commitMsg = "\"Updated submodule " + projectName + " with the latest from " + self._args.gerritBranch + "\""
        git.commit_changes(commitMsg, self._repoDir)

        # set push url to remote origin
        user = "cbacomci"
        git.set_pushUrl(self._repoDir, self._args.repo, user)

        # push to gerrit or remote
        if self._args.gerritTrigger == 'review':
            pushToBranch = "HEAD:refs/for/" + self._args.comBranch
        elif self._args.gerritTrigger == 'push':
            pushToBranch = "HEAD:" + self._args.comBranch

        returnValue = git.upload_changes(pushToBranch, self._repoDir)
        if returnValue > 0:
            print("Error: Failed to upload submodule changes")
            sys.exit(1)
