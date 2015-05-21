import numpy as np
from progress_bar import *
import theano as _th


def train(dataset_x, dataset_y, model, optimiser, criterion, epoch, batch_size):
    progress = make_progressbar('Training', epoch, len(dataset_x))
    progress.start()

    shuffle = np.random.permutation(len(dataset_x))

    mini_batch_input = np.empty(shape=(batch_size, 28*28), dtype=_th.config.floatX)
    mini_batch_targets = np.empty(shape=(batch_size, ), dtype=_th.config.floatX)

    for j in range(dataset_x.shape[0] // batch_size):
        for k in range(batch_size):
            mini_batch_input[k] = dataset_x[shuffle[j * batch_size + k]]
            mini_batch_targets[k] = dataset_y[shuffle[j * batch_size + k]]

        model.zero_grad_parameters()
        model.accumulate_gradients(mini_batch_input, mini_batch_targets, criterion)
        optimiser.update_parameters(model)

        progress.update(j * batch_size)

    progress.finish()
