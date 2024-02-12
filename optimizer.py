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
    for i in range(len(real_scores)):
        real_pair = real_scores[i]
        weighted_scores = [0, 0]
        for metricname in metricnames:
            scores_pair = all_scores[metricname][i]
            weighted_scores[0] += scores_pair[0]*weights[metricname]
            weighted_scores[1] += scores_pair[1]*weights[metricname]
        if (weighted_scores[0] > weighted_scores[1] and real_pair[0] < real_pair[1]) or (weighted_scores[0] < weighted_scores[1] and real_pair[0] > real_pair[1]):
            winner += 1
    ratio = winner/len(real_scores)*100
    print("cost_function(" + str(weights_vals) + ") : " + str(ratio))
    return 100 - ratio


def train():
    print("Let's do some training!")
    weights_vals = np.array([0.0, 0.01, 0.56])
    # weights_vals initialised randomly
    # weights_vals = 

    # Minimize the cost function
    result = minimize(cost_function, weights_vals, method='L-BFGS-B')

    # Print results
    optimized_params = result.x
    minimized_cost = result.fun

    print("Best parameters:", optimized_params)
    print("Highest score:", -minimized_cost + 100)




# main
if __name__ == '__main__':
    metricnames = ["wer", "semdist", "cer"]

    all_scores = dict()
    for metricname in metricnames:
        all_scores[metricname] = read_pickle(metricname)
    real_scores = read_pickle("real")

    # print(len(all_scores["wer"]))
    # print(len(all_scores["semdist"]))
    # print(len(real_scores))

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
    for method in methods:
        print(method)
        train(method)
        print("\n-----\n")