from keras.datasets import fashion_mnist
from keras.utils import np_utils
from os import path
import sys
yourDirectory = 'path/to/library'
if path.isdir(yourDirectory):
    sys.path.insert(0, yourDirectory)
else:
    print('That is not a directory. Please enter a valid directory')
    quit()

try:
    from network import Network
    from fc_layer import FCLayer
    from conv_layer import ConvLayer
    from flatten_layer import FlattenLayer
    from activation_layer import ActivationLayer
    from activations import tanh, tanh_prime
    from losses import mse, mse_prime
except:
    print('Error installing the network libraries. Try again')
    quit()

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# training data : 60000 samples
# reshape and normalize input data 
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_train = x_train.astype('float32')
x_train /= 255
# encode output which is a number in range [0,9] into a vector of size 10
# e.g. number 3 will become [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
y_train = np_utils.to_categorical(y_train)

# same for test data : 10000 samples
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_test = x_test.astype('float32')
x_test /= 255
y_test = np_utils.to_categorical(y_test)

# Network
net = Network()
net.add(ConvLayer((28, 28, 1), (3, 3), 1))  # input_shape=(28, 28, 1)   ;   output_shape=(26, 26, 1) 
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FlattenLayer())                     # input_shape=(26, 26, 1)   ;   output_shape=(1, 26*26*1)
net.add(FCLayer(26*26*1, 100))              # input_shape=(1, 26*26*1)  ;   output_shape=(1, 100)
net.add(ActivationLayer(tanh, tanh_prime))
net.add(FCLayer(100, 10))                   # input_shape=(1, 100)      ;   output_shape=(1, 10)
net.add(ActivationLayer(tanh, tanh_prime))

net.use(mse, mse_prime)
net.fit(x_train[:10000], y_train[:10000], epochs=100, learning_rate=0.05)

out = net.predict(x_test[0:3])

print('Predicted Values:')
print(out)
print('Actual Values:')
print(y_test[0:3])

file = open('output.txt','w')
file.write(str(out))
file.write(str(y_test[0:3]))
file.close()