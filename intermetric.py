import pickle


def read_pickle(metricname):
    # read pickle
    with open("datasets/scores/" + metricname + ".pickle", "rb") as file:
        scores = pickle.load(file)
    return scores

def get_agreement(scores1, scores2):
    assert len(scores1) == len(scores2)
    agree = 0
    disagree = 0

    for i in range(len(scores1)):
        score1_A = scores1[i][0]
        score1_B = scores1[i][1]
        score2_A = scores2[i][0]
        score2_B = scores2[i][1]
        if score1_A < score1_B and not (score2_A < score2_B):
            disagree += 1
        elif score1_A > score1_B and not (score2_A > score2_B):
            disagree += 1
        elif score1_A == score1_B and not (score2_A == score2_B):
            disagree += 1
        else:
            agree += 1
    return agree/(agree+disagree)*100



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

    # print(len(all_scores["wer"]))
    # print(len(all_scores["cer"]))
    # print(len(all_scores["phoner"]))
    # print(len(all_scores["semdist"]))
    # print(len(all_scores["semdist_multi"]))
    # print(len(real_scores))

    agreements = dict() # dict of dict - agreements["wer"]["cer"] = agreement
    for metricname1 in metricnames:
        if metricname1 not in agreements:
            agreements[metricname1] = dict()
        for metricname2 in metricnames:
            # if metricname1 == metricname2:
            #     continue
            agreement = get_agreement(all_scores[metricname1], all_scores[metricname2])
            if metricname2 not in agreements[metricname1]:
                agreements[metricname1][metricname2] = agreement
        agreement = get_agreement(all_scores[metricname1], real_scores)
        agreements[metricname1]["real"] = agreement

    # write agreements to file
    with open("results/agreements.txt", "w", encoding="utf8") as file:
        txt = ","
        for metricname in metricnames:
            txt += metricname + ","
        txt = txt[:-1] + "\n"
        for metricname1 in metricnames:
            txt += metricname1 + ","
            for metricname2 in metricnames:
                txt += str(agreements[metricname1][metricname2]) + ","
            txt = txt[:-1] + "\n"
        file.write(txt)
