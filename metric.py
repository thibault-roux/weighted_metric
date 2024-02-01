import pickle

def read_pickle(metricname):
    # read pickle
    with open("datasets/scores/" + metricname + ".pickle", "rb") as file:
        scores = pickle.load(file)
    return scores

# main
if __name__ == '__main__':
    metricnames = ["wer", "semdist"]

    all_scores = dict()
    for metricname in metricnames:
        all_scores[metricname] = read_pickle(metricname)
        print(len(all_scores[metricname]))