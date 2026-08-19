import numpy as np

def activationFunction(z):
    #sigmoid
    #return 1/(1+(np.exp(-z)))
    #tanh
    return (2/(1+(np.exp(-2*z))))-1

def derivativeActivationFunction(z):
    #tanh'
    return 1 - (activationFunction(z)**2)

class Layer:
    def __init__(self, width, inputwidth):
        self.weights = np.random.uniform(-1, 1, (width, inputwidth))
        self.biases = np.random.uniform(-1, 1, width)

    def result(self, inputData):
        data = activationFunction((self.weights @ inputData) + self.biases)
        return data

class Model:
    def __init__(self, layers):
        self.layers = layers

    def forward(self, input):
        data = input.reshape(42)
        for layer in self.layers:
            data = layer.result(data)
        return data

    def backPropagate(self, input, target):
        actualValue = self.forward(input)
        loss = 0.5*((target - actualValue)**2)
        for layer in reversed(self.layers):

