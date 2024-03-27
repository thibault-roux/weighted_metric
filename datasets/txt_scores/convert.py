import pickle



def read_hats():
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
            if dictionary["nbrA"] != dictionary["nbrB"]:
                dataset.append(dictionary)
    return dataset


def read_pickle(metricname):
    with open("../scores/" + metricname + ".pickle", "rb") as file:
        return pickle.load(file)










# main
if __name__ == '__main__':
    metricnames = ["wer", "semdist", "cer"]
    for metricname in metricnames:
        metric = read_pickle(metricname + "_Y")
        print(type(metric))
        print(len(metric))

    dataset = read_hats()
    print(len(dataset))