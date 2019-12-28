import numpy as np
from copy import deepcopy


def cal_exp(observed_map, n_mine, init_val=None):
    print(' - DECIDING WHERE TO CLICK')
    lx, ly = observed_map.shape
    if init_val is None:
        exp_map = np.ones(observed_map.shape) * 9 * n_mine
        exp_map[observed_map == -1] = 1
        exp_map = exp_map / n_mine
    else:
        exp_map = deepcopy(init_val)
        exp_map[observed_map != -1] = 9
    change, iter = 100, 0
    unclicked = {(x, y) for y in range(ly) for x in range(lx) if observed_map[x, y] == -1}

    while change >= 1e-2 and iter < 2000:
        updated = set()
        iter += 1
        change = 0
        for x in range(lx):
            for y in range(ly):
                if observed_map[x, y] > 0:
                    neighbors, neighbor_sum = [], 0
                    for xx in range(max(0, x - 1), min(lx, x + 2)):
                        for yy in range(max(0, y - 1), min(ly, y + 2)):
                            if observed_map[xx, yy] == -1:
                                neighbors.append((xx, yy))
                                neighbor_sum += exp_map[xx, yy]
                    for xx, yy in neighbors:
                        elm = exp_map[xx, yy] / neighbor_sum * observed_map[x, y]
                        elm = max(0., elm)
                        elm = min(1., elm)
                        # change += abs(elm - exp_map[xx, yy])
                        exp_map[xx, yy] = elm
                        updated.add((xx, yy))

        updated_sum = 0
        for xx, yy in updated:
            updated_sum += exp_map[xx, yy]
        else_exp = (n_mine - updated_sum) / (len(unclicked) - len(updated)) if len(unclicked) > len(updated) else 0
        else_exp = max(min(1, else_exp), 0)
        for xx, yy in unclicked:
            if (xx, yy) not in updated:
                change += abs(else_exp - exp_map[xx, yy])
                exp_map[xx, yy] = else_exp
        # print('ITERATION:', iter, '   CHANGE:', change)
        # print(exp_map)
    # print(exp_map)
    print('  - ITERATION:', iter)
    return exp_map


def strategy(observed_map, n_mine, init=None):
    lx, ly = observed_map.shape
    exp_map = cal_exp(observed_map, n_mine, init)
    pos = np.argmax(-exp_map)
    return (pos // ly, pos % ly), exp_map


if __name__ == '__main__':
    tst_set = np.array([
        [-1, -1, -1, -1],
        [-1, 4, -1, -1],
        [-1, -1, 3, 2],
        [-1, -1, 1, 0]
    ])
    # cal_exp(tst_set, 5)
    # print(np.argmax(tst_set))
    # p = strategy(tst_set, 5)
    # print(p)
    unclicked = {(x, y) for y in range(4) for x in range(4) if tst_set[x, y] != -1}
    print(unclicked)

