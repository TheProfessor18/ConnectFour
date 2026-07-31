import numpy as np

def activationFunction(z):
    #sigmoid
    return 1/(1+(np.exp(-z)))

class Layer:
    def __init__(self, width, inputwidth):
        self.weights = np.random.uniform(-1, 1, (width, inputwidth))
        self.biases = np.random.uniform(-1, 1, width)

    def result(self, inputData):
        data = activationFunction((self.weights @ inputData) + self.biases)
        return data

class Model:
    def __init__(self, hiddenLayers, hiddenWidth):
        self.layers = [
            Layer(16, 42),
            Layer(16,16),
            Layer(16,16),
            Layer(7, 16)
        ]

    def forward(self, input):
        data = input.reshape(42)
        for layer in self.layers:
            data = layer.result(data)
        return data

    def backPropagate(self, index, loss):
        pass
