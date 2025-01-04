import numpy as np

def max_consecutive_numpy(lst, instances):
    # Convert the list to a numpy array
    arr = np.array(lst)
    
    # Initialize variables to keep track of the maximum consecutive zeros
    max_zeros = 0
    current_zeros = 0
    
    # Iterate over the array
    for value in arr:
        if value == instances:
            current_zeros += 1
            max_zeros = max(max_zeros, current_zeros)  # Update the maximum if needed
        else:
            current_zeros = 0  # Reset the count when a non-zero value is found
    
    return max_zeros