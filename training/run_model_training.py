from config import MODEL_PATH_WEIGHTS, MODEL_PATH_ARCHITECTURE
from training.model_training import load_vgg_model, train_model, save_model

model = load_vgg_model()
model.summary()
train_model(model)
save_model(model, MODEL_PATH_WEIGHTS, MODEL_PATH_ARCHITECTURE)
