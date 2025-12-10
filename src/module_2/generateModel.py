from lib.model.Model import Model
from lib.config.ConfigParser import ConfigParser

# Script that shows the usage of Model to create a model of a single microphone
config = ConfigParser()

model = Model(config, True)
model.import_csv(".\\src\\module_2\\model_params.csv")
model.set_n(config.HeartSoundModel.NBeats)
model.save()