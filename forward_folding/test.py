import numpy as np

def compute_reward(path, sequence):
    """ Match the sequence to each paths and compute the energy. Return all minimum energy structures. Stores paths in a heap.
    H-H bond = -1
    P-P bond = 0
    :param paths: list of paths that have been pre-computed by brute-force algorithm 
    :param sequence: the sequence to be folded
    :return: list of paths with minimum energy
    """

    print(path)
    print(sequence)
    H_coords_even = []
    H_coords_odd = []
    energy = 0
    j = 0  # tracks the last time we saw an H along the chain
    for i in range(len(sequence)):
        i += 1
        if sequence[i-1] == 'H':
            # Compute the energy of interaction with any Hs before it
            # curr_x, curr_y = path[i]
            curr_x, curr_y = np.where(path == i)
            if i == j + 1:  # that means that the last time we encountered an H, it was adjacent to the current H
                if i % 2 == 0: #even
                    H_coords_even.append((curr_x, curr_y))
                    for coord in H_coords_odd[:-1]:  # skip last element
                        distance = abs(curr_x - coord[0]) + abs(curr_y - coord[1])  # calculate distance between 2 Hs using city block distance
                        if distance == 1:
                            energy -= 1
                else: # odd
                    H_coords_odd.append((curr_x, curr_y))
                    for coord in H_coords_even[:-1]:  # skip last element
                        distance = (curr_x - coord[0]) ** 2 + (
                                curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                        if distance == 1:
                            energy -= 1

            else:
                if i % 2 == 0:
                    H_coords_even.append((curr_x, curr_y))
                    for coord in H_coords_odd:  # skip last element
                        distance = (curr_x - coord[0]) ** 2 + (
                                curr_y - coord[1]) ** 2  # calculate distance between 2 Hs
                        if distance == 1:
                            energy -= 1
                else:
                    H_coords_odd.append((curr_x, curr_y))
                    print(f'curr x est {H_coords_even}')
                    for coord in H_coords_even:  # skip last element
                        
                        distance = (curr_x[0] - coord[0]) ** 2 + (
                                curr_y[0] - coord[1]) ** 2  # calculate distance between 2 Hs
                        print(distance)
                        if distance == 1:
                            energy -= 1
            j = i

    return energy


if __name__ == '__main__':
    a = np.array(
        [[0,0,0,0],
         [0,1,2,0],
         [0,4,3,0],
         [0,0,0,0]]
    )
    s = 'PPPH'
    print(compute_reward(a, s))