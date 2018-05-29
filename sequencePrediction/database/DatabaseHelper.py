from enum import Enum
import os
from random import shuffle
from sequencePrediction.predictor.profile.Profile import Profile

from database.SequenceDatabase import SequenceDatabase


class DatabaseHelper(object):
    basePath = None
    database = None

    class Format(Enum):
        BIBLE = 1
        BMS = 2
        FIFA = 3
        KOSARAK = 4
        LEVIATHAN = 5
        MSNBC = 6
        SIGN = 7
        CUSTOM=8

    def __init__(self, basePath):
        """ generated source for method __init__ """
        self.basePath = basePath
        self.database = SequenceDatabase()
        self.database.parameters = dict()

    def getDatabase(self):
        return self.database

    def loadDataset(self, fileName, maxCount):
        # Clearing the database
        if self.database == None:
            self.database = SequenceDatabase()
        else:
            self.database.clear()

        # Tries to guess the format if it is a predefined dataset
        try:
            # datasetFormat = self.Format.valueOf(fileName)
            datasetFormat = getattr(self.Format, fileName)
            self.loadPredefinedDataset(datasetFormat, maxCount)
        except ValueError:
            loadCustomDataset(fileName, maxCount)
        # Shuffling the database
        shuffle(self.database.getSequences())


    def loadCustomDataset(self, fileName, maxCount):
        """ generated source for method loadCustomDataset """
        try:
            self.database.loadFileCustomFormat(fileToPath(fileName), maxCount, Profile.paramInt("sequenceMinSize"), Profile.paramInt("sequenceMaxSize"))
        except IOError as e:
            print("Could not load dataset, IOExeption")
            e.printStackTrace()

    # 
    # 	 
    def loadPredefinedDataset(self, format, maxCount):
        """ generated source for method loadPredefinedDataset """
        # Loading the specified dataset (according to the format)
        try:
            if format == self.Format.BMS:
                self.database.loadFileDefaultFormat(self.fileToPath("BMS.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.KOSARAK:
                self.database.loadFileDefaultFormat(self.fileToPath("KOSARAK.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.FIFA:
                self.database.loadFileDefaultFormat(self.fileToPath("FIFA.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.MSNBC:
                self.database.loadFileDefaultFormat(self.fileToPath("msnbc.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.SIGN:
                self.database.loadFileDefaultFormat(self.fileToPath("SIGN.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.BIBLE:
                self.database.loadFileDefaultFormat(self.fileToPath("BIBLE.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            elif format == self.Format.LEVIATHAN:
                self.database.loadFileDefaultFormat(self.fileToPath("LEVIATHAN.dat"), maxCount, self.Profile.paramInt("sequenceMinSize"), self.Profile.paramInt("sequenceMaxSize"))
            else:
                print("Could not load dataset, unknown format.")
        except IOError as e:
            print("Could not load dataset, IOExeption")
            e.printStackTrace()

    #  
    # 	 * Return the path for the specified data set file
    # 	 * @param filename Name of the data set file
    # 	 * @throws UnsupportedEncodingException 
    # 	 
    def fileToPath(self, filename):
        """ generated source for method fileToPath """
        return os.path.join(self.basePath, filename)
#
# DatabaseHelper.# 	 * Loads a predefined dataset -- see full list in DatabaseHelper.Format

