import pickle
from itertools import product
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.optimize import minimize



def read_pickle(metricname):
    # read pickle
    with open("datasets/scores/" + metricname + ".pickle", "rb") as file:
        scores = pickle.load(file)
    return scores



def cost_function(weights_vals):
    # weights_vals = [0.3213, 0.014423, 0.99999] # example of weights
    weights = dict()
    for i in range(len(metricnames)):
        weights[metricnames[i]] = weights_vals[i]
    # weighted scores
    winner = 0
    for i in range(len(train_real_scores)):
        real_pair = train_real_scores[i]
        weighted_scores = [0, 0]
        for metricname in metricnames:
            scores_pair = train_all_scores[metricname][i]
            weighted_scores[0] += scores_pair[0]*weights[metricname]
            weighted_scores[1] += scores_pair[1]*weights[metricname]
        if (weighted_scores[0] > weighted_scores[1] and real_pair[0] < real_pair[1]) or (weighted_scores[0] < weighted_scores[1] and real_pair[0] > real_pair[1]):
            winner += 1
    ratio = winner/len(train_real_scores)*100
    # print("cost_function(" + str(weights_vals) + ") : " + str(ratio))
    return 100 - ratio


def test_function(weights_vals):
    # weights_vals = [0.3213, 0.014423, 0.99999] # example of weights
    weights = dict()
    for i in range(len(metricnames)):
        weights[metricnames[i]] = weights_vals[i]
    # weighted scores
    winner = 0
    for i in range(len(test_real_scores)):
        real_pair = test_real_scores[i]
        weighted_scores = [0, 0]
        for metricname in metricnames:
            scores_pair = test_all_scores[metricname][i]
            weighted_scores[0] += scores_pair[0]*weights[metricname]
            weighted_scores[1] += scores_pair[1]*weights[metricname]
        if (weighted_scores[0] > weighted_scores[1] and real_pair[0] < real_pair[1]) or (weighted_scores[0] < weighted_scores[1] and real_pair[0] > real_pair[1]):
            winner += 1
    ratio = winner/len(test_real_scores)*100
    # print("cost_function(" + str(weights_vals) + ") : " + str(ratio))
    return ratio


def train(method, best):
    # x1 = 0.000001
    # x2 = 0.00101608
    # x3 = 0.06685642
    x1 = 0.5
    x2 = 0.5
    x3 = 0.5
    x4 = 0.5
    # 95.14824797843666
    # [-0.09363871  0.01798104  0.90433826  2.9213723 ]
    std = 0.5
    # weights_vals = np.array([x1 + np.random.normal(x1, std), x2 + np.random.normal(x2, std), x3 + np.random.normal(x3, std), x4 + np.random.normal(x4, std)])
    # weights_vals initialised randomly
    weights_vals = np.random.uniform(0, 1, 4)

    # Minimize the cost function
    result = minimize(cost_function, weights_vals, method=method)

    # Print results
    optimized_params = result.x
    minimized_cost = result.fun

    # print("Best parameters:", optimized_params)
    # print("Highest score:", -minimized_cost + 100)

    newbest = -minimized_cost + 100
    parameters = optimized_params
    return newbest, parameters



def negative_sum(X):
    negsum = 0
    for x in X:
        if x < 0:
            negsum -= x
    return negsum


# main
if __name__ == '__main__':
    metricnames = ["wer_Y", "semdist_Y", "cer_Y", "phoner_Y"]

    all_scores = dict()
    for metricname in metricnames:
        all_scores[metricname] = read_pickle(metricname)
    real_scores = read_pickle("real_Y")

    # split in train and val sets ----------------
    splitter = int(len(real_scores)*0.5)

    train_real_scores = real_scores[:splitter]
    test_real_scores = real_scores[splitter:]
    train_all_scores = dict()
    test_all_scores = dict()
    for metricname in metricnames:
        train_all_scores[metricname] = all_scores[metricname][:splitter]
        test_all_scores[metricname] = all_scores[metricname][splitter:]


    # Compute score for all metrics ----------------
    real_scores = real_scores
    winner = dict()
    for metricname in metricnames:
        winner[metricname] = 0
    # scores for all metrics
    for i in range(len(real_scores)):
        real_pair = real_scores[i]
        for metricname in metricnames:
            scores_pair = all_scores[metricname][i]
            if (scores_pair[0] > scores_pair[1] and real_pair[0] < real_pair[1]) or (scores_pair[0] < scores_pair[1] and real_pair[0] > real_pair[1]):
                winner[metricname] += 1
    for metricname in metricnames:
        print(metricname, winner[metricname]/len(real_scores)*100)



    methods = ["Nelder-Mead", "Powell", "CG", "BFGS", "Newton-CG", "L-BFGS-B", "TNC", "COBYLA", "SLSQP", "trust-const", "dogleg", "trust-ncg", "trust-exact", "trust-krylov"]
    removes = ["Newton-CG", "trust-const", "dogleg", "trust-ncg", "trust-exact", "trust-krylov"]
    for remove in removes:
        methods.remove(remove)

    best = 0
    best_parameters = (0, 0, 0)
    while True:
        for method in methods:
            newbest, parameters = train(method, best)
            if newbest > best or (newbest == best and negative_sum(parameters) < negative_sum(best_parameters)):
                print(method)
                print("newbest:", newbest)
                print("parameters:", parameters)
                test_score = test_function(parameters)
                print("test_score:", test_score)
                best = newbest
                best_parameters = parameters
                print("\n-----\n")