from components.model_training import load_vgg_model, train_model, save_model

model = load_vgg_model()
model.summary()
train_model(model)
save_model(model, 'model_weights.h5', 'model_architecture.json')
