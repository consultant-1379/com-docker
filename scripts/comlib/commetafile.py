import json

class ComMetaFile:

    _BUILD="build"
    _IMAGE="image"
    _COMMIT="commit"
    _REPOSITORY="repository"

    def __init__(self):
        self._meta = {}

    def load(self, filename):
        print "loading from: " + filename
        f = open(filename, "r")
        self._meta = json.load(f)

    def write(self, filename):
        print "writing to: " + filename
        jsondata = json.dumps(self._meta, sort_keys=True, indent=4, separators=(',', ':') )
        f = open(filename, "w")
        f.write(jsondata)
        f.close()

    def printInfo(self):
        print json.dumps(self._meta, sort_keys=True, indent=4, separators=(',', ':') )

    def _addInfo(self, location, repository, commit):
        self._meta[location] = {}
        self._meta[location][self._REPOSITORY] = repository
        self._meta[location][self._COMMIT] = commit

    def addBuildInfo(self, repository, commit):
        self._addInfo(self._BUILD, repository, commit)

    def addImageInfo(self, repository, commit):
        self._addInfo(self._IMAGE, repository, commit)

    def _getInfo(self, location, key):
        return self._meta[location][key]

    def getBuildCommit(self):
        return self._getInfo(self._BUILD, self._COMMIT)

    def getBuildRepository(self):
        return self._getInfo(self._BUILD, self._REPOSITORY)

    def getImageCommit(self):
        return self._getInfo(self._IMAGE, self._COMMIT)

    def getImageRepository(self):
        return self._getInfo(self._IMAGE, self._REPOSITORY)
