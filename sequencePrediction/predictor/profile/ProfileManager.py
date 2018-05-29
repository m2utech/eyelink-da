from sequencePrediction.predictor.profile.DefaultProfile import DefaultProfile
from sequencePrediction.predictor.profile.MSNBCProfile import MSNBCProfile
from sequencePrediction.predictor.profile.BMSProfile import BMSProfile
from sequencePrediction.predictor.profile.BIBLEProfile import BIBLEProfile
from sequencePrediction.predictor.profile.FIFAProfile import FIFAProfile
from sequencePrediction.predictor.profile.KOSARAKProfile import KOSARAKProfile
from sequencePrediction.predictor.profile.SIGNProfile import SIGNProfile

class ProfileManager:

    def loagProfileByName(self, name):
        profile = None
        try:
            classI = eval('{}Profile'.format(name))
            profile = classI()
        except:
            profile = DefaultProfile()
        profile.Apply()
        return profile

if __name__=='__main__':
    aa = ProfileManager()
    aa.loagProfileByName("MSNBC")
