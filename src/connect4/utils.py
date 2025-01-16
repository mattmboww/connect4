import math

def sigmoid(x, lambda_ = 1):
  return 2 / (1 + math.exp(-lambda_ * (x-0.5))) - 1
