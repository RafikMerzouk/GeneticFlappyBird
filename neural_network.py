import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_to_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_to_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

    def feedforward(self, inputs):
        self.hidden = sigmoid(np.dot(inputs, self.weights_input_to_hidden) + self.bias_hidden)
        self.output = sigmoid(np.dot(self.hidden, self.weights_hidden_to_output) + self.bias_output)
        return self.output

    def predict(self, inputs):
        if self.feedforward(inputs) > 0.5:
            return 1  # Jump
        else:
            return 0  # Do not jump

    def mutate(self, mutation_rate):
        for weight_matrix in [self.weights_input_to_hidden, self.weights_hidden_to_output]:
            for i in range(weight_matrix.shape[0]):
                for j in range(weight_matrix.shape[1]):
                    if np.random.rand() < mutation_rate:
                        weight_matrix[i][j] += np.random.randn() * 0.5

        for bias in [self.bias_hidden, self.bias_output]:
            for i in range(len(bias)):
                if np.random.rand() < mutation_rate:
                    bias[i] += np.random.randn() * 0.5