import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  num_train = X.shape[0]
  num_classes = W.shape[1]
  
  for i in range(num_train):
    scores = X[i].dot(W)
    exp_scores = np.exp(scores)
    exp_correct_class = exp_scores[y[i]]
    sum_exp_scores = np.sum(exp_scores)
    
    loss += - np.log(exp_correct_class / sum_exp_scores) 
    
    for j in range(num_classes):
        if j == y[i]:
            dW[:, j] += -X[i].T

        dW[:, j] += X[i].T * exp_scores[j] / sum_exp_scores 
  
  loss /= num_train
  dW /= num_train

  loss += reg * np.sum(W**2)
  dW += 2 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  num_train = X.shape[0]
  num_classes = W.shape[1]
  
  scores = X.dot(W)
  correct_class_scores = scores[range(X.shape[0]), y].reshape(-1,1)
  # it's important for broadcasting to reshape the (N, )-array into (N, 1)-array
  
  exp_scores = np.exp(scores)
  exp_correct_class = np.exp(correct_class_scores)
  sum_exp_scores = np.sum(exp_scores, axis=1).reshape(-1,1)
  
  loss = - np.sum(np.log(exp_correct_class / sum_exp_scores)) / num_train + reg * np.sum(W**2)

  nonzero_entries = np.zeros((num_train, num_classes))
  nonzero_entries = exp_scores / sum_exp_scores
  nonzero_entries[range(num_train), y] -= 1
  
  dW = (X.T).dot(nonzero_entries) / num_train + 2 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

