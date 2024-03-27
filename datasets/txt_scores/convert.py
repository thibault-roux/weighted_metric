import pickle



def read_hats(certitude=0.7):
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open("../hats.txt", "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hypA"] = line[1]
            dictionary["nbrA"] = int(line[2])
            dictionary["hypB"] = line[3]
            dictionary["nbrB"] = int(line[4])

            nbrA = dictionary["nbrA"]
            nbrB = dictionary["nbrB"]
            maximum = max(nbrA, nbrB)
            c = maximum/(nbrA+nbrB)
            if c >= certitude:
                dataset.append(dictionary)
    return dataset


def read_pickle(metricname):
    with open("../scores/" + metricname + ".pickle", "rb") as file:
        return pickle.load(file)




# main
if __name__ == '__main__':
    metricnames = ["wer", "cer", "phoner", "semdist"]
    ALL_scores = dict()
    for metricname in metricnames:
        ALL_scores[metricname] = read_pickle(metricname + "_Y")

    dataset = read_hats()

    with open("scores.txt", "w", encoding="utf8") as file:
        txt = ""
        for metricname in metricnames:
            txt += metricname + ","
        txt = txt[:-1] + "\n"
        i = 0
        for item in dataset:
            for metricname in metricnames:
                txt += str(ALL_scores[metricname][i][0]) + ","
            txt = txt[:-1] + "\n"
            for metricname in metricnames:
                txt += str(ALL_scores[metricname][i][1]) + ","
            txt = txt[:-1] + "\n"
        file.write(txt)
    print("Done")