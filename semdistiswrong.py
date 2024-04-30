import pickle


def read_pickle(metricname):
    # read pickle
    with open("datasets/scores/" + metricname + ".pickle", "rb") as file:
        scores = pickle.load(file)
    return scores


def agree(score1, score2):
    score1_A, score1_B = score1
    score2_A, score2_B = score2
    if score1_A < score1_B and not (score2_A < score2_B):
        return False
    elif score1_A > score1_B and not (score2_A > score2_B):
        return False
    elif score1_A == score1_B and not (score2_A == score2_B):
        return False
    else:
        return True

def agreement_if_wrong(scores_wrong, scores, real):
    if len(scores_wrong) != len(scores) or len(scores) != len(real):
        raise ValueError("Lengths of scores_wrong, scores and real should be equal"

    agree_wrong = 0
    disagree_wrong = 0
    for i in range(len(scores)):
        if not agree(scores_wrong[i], real[i]): # scores is wrong
            if agree(scores[i], real[i]): # scores is correct
                agree_wrong += 1
            else:
                disagree_wrong += 1 # scores is also wrong
    return agree_wrong/(agree_wrong+disagree_wrong)*100

# main
if __name__ == '__main__':
    metricnames = ["wer", "cer", "phoner", "semdist", "semdist_multi"]

    all_scores = dict()
    for metricname in metricnames:
        all_scores[metricname] = read_pickle(metricname + "_Z")
    real_scores = read_pickle("real_Z")
    # convert all values of real_scores to negative
    for i in range(len(real_scores)):
        real_scores[i] = (-real_scores[i][0], -real_scores[i][1])
