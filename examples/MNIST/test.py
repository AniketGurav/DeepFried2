import numpy as np
from progress_bar import *
import theano as _th
from sklearn.metrics import accuracy_score

def validate(dataset_x, dataset_y, model, epoch, batch_size):
    progress = make_progressbar('Testing', epoch, len(dataset_x))
    progress.start()

    mini_batch_input = np.empty(shape=(batch_size, 28*28), dtype=_th.config.floatX)
    mini_batch_targets = np.empty(shape=(batch_size, ), dtype=_th.config.floatX)
    accuracy = 0

    for j in range((dataset_x.shape[0] + batch_size - 1) // batch_size):
        progress.update(j * batch_size)
        for k in range(batch_size):
            if j * batch_size + k < dataset_x.shape[0]:
                mini_batch_input[k] = dataset_x[j * batch_size + k]
                mini_batch_targets[k] = dataset_y[j * batch_size + k]

        mini_batch_prediction = np.argmax(model.forward(mini_batch_input), axis=1)

        if (j + 1) * batch_size > dataset_x.shape[0]:
            mini_batch_prediction.resize((dataset_x.shape[0] - j * batch_size, ))
            mini_batch_targets.resize((dataset_x.shape[0] - j * batch_size, ))

        accuracy = accuracy + accuracy_score(mini_batch_targets, mini_batch_prediction, normalize=False)

    progress.finish()
    print("Epoch #" + str(epoch) + ", Classification: " + str(float(accuracy) / dataset_x.shape[0] * 100.0))
