import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

class Node:
    def __init__(self, weightsCount):
        self.weights = np.zeros(weightsCount)
        self.bias = 0

class Layer:
    def __init__(self, nodesCount, previousLayer):
        self.nodes = np.array([Node(len(previousLayer)) for _ in range(nodesCount)])


inputLayer = np.zeros(42)
hiddenLayer1 = Layer(16, inputLayer)
hiddenLayer2 = Layer(16, hiddenLayer1.nodes)
outputLayer = Layer(8, hiddenLayer2.nodes)

def getIntensities(input, layer):
    output = []
    for node in layer.nodes:
        dotProd = np.dot(node.weights, input)
        addBias = dotProd + node.bias
        output.append(sigmoid(addBias))
    return output

round1 = getIntensities(inputLayer, hiddenLayer1)
round2 = getIntensities(round1, hiddenLayer2)
result = getIntensities(round2, outputLayer)

print(result)