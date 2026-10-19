import os
from pathlib import Path
import random
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

data_file = Path(r'names.txt')
seed = 2147483647
g = torch.Generator().manual_seed(seed)
random.seed(seed)

'''
train test splitting at word/name level
'''
def prepare_data(split=None):
    words = open(data_file, 'r').read().splitlines()
    random.shuffle(words)
    num_words = len(words)
    
    all_chars = sorted(list(set(''.join(words))))
    char_to_idx = {c: i+1 for i, c in enumerate(all_chars)}
    char_to_idx['.'] = 0
    idx_to_char = {i: c for c, i in char_to_idx.items()}
    
    if split == 'default':
        train_idx = int(0.8 * num_words)
        val_idx = int(0.9 * num_words)
        train_words = words[:train_idx]
        val_words = words[train_idx:val_idx]
        test_words = words[val_idx:]
        return train_words, val_words, test_words, char_to_idx, idx_to_char
    else:
        return words, char_to_idx, idx_to_char

'''
create a bigram and trigram matrix from the data
'''
def get_bigram_matrix(words, char_to_idx, smoothing=1.0):
    N = smoothing * torch.ones((27, 27)).float()
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2 in zip(chars, chars[1:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            N[idx1, idx2] += 1
    return N

def get_trigram_matrix(words, char_to_idx, smoothing=1.0):
    N = smoothing * torch.ones((27, 27, 27)).float()
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2, ch3 in zip(chars, chars[1:], chars[2:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            idx3 = char_to_idx[ch3]
            N[idx1, idx2, idx3] += 1
    return N

'''
sampling using the bigram and trigram count matrices
for trigram count matrix, the second character of the first word is chosen at random from the 26 alphabets
'''
def bigram_sampling(bigram_matrix, idx_to_char, num_words=10):
    probs = bigram_matrix/bigram_matrix.sum(dim=1, keepdims=True)
    for _ in range(num_words):
        idx = 0
        out = []
        while True:
            p = probs[idx]
            idx = torch.multinomial(p, num_samples=1, replacement=True, generator=g).item()
            out.append(idx_to_char[idx])
            if idx == 0:
                break
        print(''.join(out))
    return

def trigram_sampling(trigram_matrix, idx_to_char, num_words=10):
    uniform_prob = torch.ones(26).float() * (1.0/26)
    for _ in range(num_words):
        idx1 = 0
        idx2 = torch.multinomial(uniform_prob, num_samples=1, replacement=True, generator=g).item() + 1
        out = [idx_to_char[idx2]]
        while True:
            p = trigram_matrix[idx1, idx2, :]
            probs = p/p.sum()
#             print(probs.sum().item())
#             assert probs.sum().item() == 1.0
            idx3 = torch.multinomial(probs, num_samples=1, replacement=True, generator=g).item()
            out.append(idx_to_char[idx3])
            if idx3 == 0:
                break
            idx1 = idx2
            idx2 = idx3
        print(''.join(out))
    return

'''
compute the negative log likelihood loss of 
'''
def compute_bigram_matrix_loss(words, bigram_matrix, char_to_idx):
    logprob = 0.0
    num_bigrams = 0
    probs = bigram_matrix/bigram_matrix.sum(dim=1, keepdims=True)
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2, ch3 in zip(chars, chars[1:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            logprob += torch.log(probs[idx1, idx2]).item()
            num_bigrams += 1
    loss = -logprob/num_bigrams
    return loss

def compute_trigram_matrix_loss(words, trigram_matrix, char_to_idx):
    logprob = 0.0
    num_trigrams = 0
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2, ch3 in zip(chars, chars[1:], chars[2:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            idx3 = char_to_idx[ch3]
            P = trigram_matrix[idx1, idx2, :]
            probs = P/P.sum()
#             print(probs.sum().item())
#             assert probs.sum().item() == 1.0
            logprob += torch.log(probs[idx3]).item()
            num_trigrams += 1
    loss = -logprob/num_trigrams
    return loss

'''
create dataset of bigrams and trigrams for neural network training
'''
def create_bigram_dataset(words, char_to_idx):
    xs, ys = [], []
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2 in zip(chars, chars[1:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            xs.append(idx1)
            ys.append(idx2)
    xs = torch.tensor(xs)
    ys = torch.tensor(ys)
    return xs, ys

def create_trigram_dataset(words, char_to_idx):
    xs, ys, zs = [], [], []
    for w in words:
        chars = ['.'] + list(w) + ['.']
        for ch1, ch2, ch3 in zip(chars, chars[1:], chars[2:]):
            idx1 = char_to_idx[ch1]
            idx2 = char_to_idx[ch2]
            idx3 = char_to_idx[ch3]
            xs.append(idx1)
            ys.append(idx2)
            zs.append(idx3)
    xs = torch.tensor(xs)
    ys = torch.tensor(ys)
    zs = torch.tensor(zs)
    return xs, ys, zs

'''
create and train a bigram or a trigram neural network model
'''
def bigram_nn_train(train_data, val_data=None, test_data=None, epochs=100, lr=50, reg=0.01, verbose=True):
    W = torch.randn((27, 27), generator=g, requires_grad=True) 
    xs, ys = train_data
    Xs = F.one_hot(xs, num_classes=27).float()
    Ys = F.one_hot(ys, num_classes=27).float()
    train_losses, test_losses, val_losses = [], [], []

    # training loop
    for i in range(epochs):
        # forward pass with softmax activation
        X1 = Xs @ W
        Xhat = X1.exp()
        probs = Xhat/Xhat.sum(dim=1, keepdims=True)

        # loss computation with regularization 
        loss = -probs[torch.arange(xs.shape[0]), ys].log().mean() + reg * (W ** 2).mean()
        train_losses.append(loss.item())

        # backpropagation
        W.grad = None # zero out the grads
        loss.backward()
        W.data -= lr * W.grad
        
        # if val data is present
        if val_data:
            xv, yv = val_data
            Xv = F.one_hot(xv, num_classes=27).float()
            X1 = Xv @ W
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True)
            loss = -probs[torch.arange(xv.shape[0]), yv].log().mean() + reg * (W ** 2).mean()
            val_loss = loss.item()
            val_losses.append(val_loss)
        else:
            val_loss = 0.0
            
        # if test data is present
        if test_data:
            xt, yt = test_data
            Xt = F.one_hot(xt, num_classes=27).float()
            X1 = Xt @ W
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True)
            loss = -probs[torch.arange(xt.shape[0]), yt].log().mean() + reg * (W ** 2).mean()
            test_loss = loss.item()
            test_losses.append(test_loss)
        else:
            test_loss = 0.0

        if (i+1)%10 == 0 and verbose:
            print_str = f'Iteration {i+1}: Train Loss {loss :.4f}'
            if val_data and test_data:
                print_str += f' Val Loss {val_loss :.4f} Test Loss {test_loss :.4f}'
            print(print_str)
    return W, train_losses, val_losses, test_losses

def trigram_nn_train(train_data, val_data=None, test_data=None, epochs=100, lr=50, reg=0.01, verbose=True):
    W = torch.randn((54, 27), generator=g, requires_grad=True) 
    xs, ys, zs = train_data
    Xs = F.one_hot(xs, num_classes=27).float()
    Ys = F.one_hot(ys, num_classes=27).float()
    XT = torch.cat([Xs, Ys], dim=1)
    train_losses, test_losses, val_losses = [], [], []

    # training loop
    for i in range(epochs):
        # forward pass with softmax activation
        X1 = XT @ W
        Xhat = X1.exp()
        probs = Xhat/Xhat.sum(dim=1, keepdims=True)

        # loss computation with regularization 
        loss = -probs[torch.arange(xs.shape[0]), zs].log().mean() + reg * (W ** 2).mean()
        train_losses.append(loss.item())

        # backpropagation
        W.grad = None # zero out the grads
        loss.backward()
        W.data -= lr * W.grad
        
        # if val data is present
        if val_data:
            xv, yv, zv = val_data
            Xv = F.one_hot(xv, num_classes=27).float()
            Yv = F.one_hot(yv, num_classes=27).float()
            XV = torch.cat([Xv, Yv], dim=1)
            X1 = XV @ W
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True)
            loss = -probs[torch.arange(xv.shape[0]), zv].log().mean() + reg * (W ** 2).mean()
            val_loss = loss.item()
            val_losses.append(val_loss)
        else:
            val_loss = 0.0
            
        # if test data is present
        if test_data:
            xt, yt, zt = test_data
            Xt = F.one_hot(xt, num_classes=27).float()
            Yt = F.one_hot(yt, num_classes=27).float()
            XX = torch.cat([Xt, Yt], dim=1)
            X1 = XX @ W
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True)
            loss = -probs[torch.arange(xt.shape[0]), zt].log().mean() + reg * (W ** 2).mean()
            test_loss = loss.item()
            test_losses.append(test_loss)
        else:
            test_loss = 0.0

        if (i+1)%10 == 0 and verbose:
            print_str = f'Iteration {i+1}: Train Loss {loss :.4f}'
            if val_data and test_data:
                print_str += f' Val Loss {val_loss :.4f} Test Loss {test_loss :.4f}'
            print(print_str)
    return W, train_losses, val_losses, test_losses

'''
inference/sampling from a bigram or a trigram neural network model
'''
def sample_bigram_nn(bigram_nn, idx_to_char, num_words=10):
    for i in range(num_words):
        out = []
        idx = 0
        while True:
            X = F.one_hot(torch.tensor([idx]), num_classes=27).float() # without [idx] the shape is not proper
            X1 = X @ bigram_nn
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True) # without [idx] in line 6, this step fails due to shape issues
            idx = torch.multinomial(probs, num_samples=1, replacement=True, generator=g).item()
            out.append(idx_to_char[idx])
            if idx == 0:
                break
        print(''.join(out))
    return

def sample_trigram_nn(trigram_nn, idx_to_char, num_words=10):
    uniform_prob = torch.ones(26).float() * (1.0/26)
    for i in range(num_words):
        idx1 = 0
        idx2 = torch.multinomial(uniform_prob, num_samples=1, replacement=True, generator=g).item() + 1
        out = [idx_to_char[idx2]]
        while True:
            x1 = F.one_hot(torch.tensor([idx1]), num_classes=27).float() # without [idx] the shape is not proper
            x2 = F.one_hot(torch.tensor([idx2]), num_classes=27).float()
            X = torch.cat([x1, x2], dim=1)
            X1 = X @ trigram_nn
            Xhat = X1.exp()
            probs = Xhat/Xhat.sum(dim=1, keepdims=True) # without [idx] in line 6, this step fails due to shape issues
            idx3 = torch.multinomial(probs, num_samples=1, replacement=True, generator=g).item()
            out.append(idx_to_char[idx3])
            if idx3 == 0:
                break
            idx1 = idx2
            idx2 = idx3
        print(''.join(out))
    return

'''
plot the losses from neural network training
'''
def plot_nn_losses(train_losses, val_losses=None, test_losses=None):
    plt.figure(figsize=(6, 6))
    plt.plot(train_losses, 'r-', linewidth=2, label='train')
    if val_losses and test_losses:
        plt.plot(val_losses, 'b-', linewidth=2, label='val')
        plt.plot(test_losses, 'g-', linewidth=2, label='test')
    plt.xlabel('epochs', fontsize=12)
    plt.ylabel('losses', fontsize=12)
    plt.title('Learning Curves', fontsize=16)
    plt.legend(fontsize=10)
    plt.show()
    return