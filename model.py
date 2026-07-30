import numpy as np

def activationFunction(z):
    #sigmoid
    return 1/(1+(np.exp(-z)))

class Layer:
    def __init__(self, width, inputwidth):
        self.weights = np.random.uniform(-1, 1, (width, inputwidth))
        self.biases = np.random.uniform(-1, 1, width)

class Model:
    def __init__(self, hiddenLayers, hiddenWidth):
        inputWidth = 42
        outputWidth = 7
        self.layers = np.array([])

        for x in range(hiddenLayers + 1):
            if x == 0:
                newLayer = Layer(hiddenWidth, inputWidth)
            elif x == hiddenLayers:
                newLayer = Layer(outputWidth, hiddenWidth)
            else:
                newLayer = Layer(hiddenWidth, hiddenWidth)

            np.append(self.layers, newLayer)

    def result(self, inputData):
        data = inputData
        for layer in self.layers:
            data = activationFunction((layer.weights @ data) + layer.biases)
        return data
