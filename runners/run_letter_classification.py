import numpy as np
from components.letter_classification import predict_letters


input_letters = np.load('letters.npy')
output = predict_letters(input_letters)
assert output.shape == (2, 28)
