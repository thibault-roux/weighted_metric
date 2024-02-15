import progressbar
import numpy
import pickle
import jiwer


def read_dataset(dataname):
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open("datasets/" + dataname, "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hypA"] = line[1]
            dictionary["nbrA"] = int(line[2])
            dictionary["hypB"] = line[3]
            dictionary["nbrB"] = int(line[4])
            dataset.append(dictionary)
    return dataset


def semdist(ref, hyp, memory):
    model, dicosave = memory
    try:
        tempdico = dicosave[ref]
        print(tempdico)
        try:
            score = tempdico[hyp] # i.e. dicosave[ref][hyp]
            return score
        except KeyError:
            flag = True
    except KeyError:
        # flag = True
        dicosave[ref] = dict()
    
    ref_projection = model.encode(ref).reshape(1, -1)
    hyp_projection = model.encode(hyp).reshape(1, -1)
    score = cosine_similarity(ref_projection, hyp_projection)[0][0]
    score = (1-score)*100 # lower is better
    dicosave[ref][hyp] = score
    return score


def wer(ref, hyp, memory):
    return jiwer.wer(ref, hyp)

def cer(ref, hyp, memory):
    return jiwer.cer(ref, hyp)

def phoner(ref, hyp, memory):
    ep = memory
    ref_phon = ep.transliterate(ref)
    hyp_phon = ep.transliterate(hyp)
    return cer(ref_phon, hyp_phon)


def evaluator(metric, metricname, dataset, memory=0, certitude=0.7, verbose=True):
    print("certitude: ", certitude*100)
    ignored = 0
    accepted = 0
    correct = 0
    incorrect = 0
    egal = 0

    all_scores = []
    real_scores = []

    if verbose:
        bar = progressbar.ProgressBar(max_value=len(dataset))
    for i in range(len(dataset)):
        if verbose:
            bar.update(i)
        nbrA = dataset[i]["nbrA"]
        nbrB = dataset[i]["nbrB"]
        
        if nbrA+nbrB < 5:
            ignored += 1
            continue
        maximum = max(nbrA, nbrB)
        c = maximum/(nbrA+nbrB)
        if c >= certitude: # if humans are certain about choice
            accepted += 1
            scoreA = metric(dataset[i]["reference"], dataset[i]["hypA"], memory=memory)
            scoreB = metric(dataset[i]["reference"], dataset[i]["hypB"], memory=memory)
            all_scores.append((scoreA, scoreB))
            real_scores.append((nbrA, nbrB))
            if (scoreA < scoreB and nbrA > nbrB) or (scoreB < scoreA and nbrB > nbrA):
                correct += 1
            elif scoreA == scoreB:
                egal += 1
            else:
                incorrect += 1
            continue
        else:
            ignored += 1

    with open("datasets/scores/" + metricname + ".pickle", "wb") as file:
        pickle.dump(all_scores, file)

    with open("datasets/scores/real.pickle", "wb") as file:
        pickle.dump(real_scores, file)

    print()
    print("correct:", correct)
    print("incorrect:", incorrect)
    print("egal:", egal)
    print("ratio correct:", correct/(correct+incorrect+egal)*100)
    print("ratio egal: ", egal/(correct+incorrect+egal)*100)
    print()
    print("ratio ignored:", ignored/(ignored+accepted)*100)
    print("ignored:", ignored)
    print("accepted:", accepted)
    return correct/(correct+incorrect+egal)*100


def write(namefile, x, y):
    with open("results/" + namefile + ".txt", "w", encoding="utf8") as file:
        file.write(namefile + "," + str(x) + "," + str(y) + "\n")


if __name__ == '__main__':
    print("Reading dataset...")
    dataset = read_dataset("hats.txt")

    cert_X = 1
    cert_Y = 0.7


    # phoner
    import epitran
    from jiwer import cer
    lang_code = 'fra-Latn-p'
    memory = epitran.Epitran(lang_code)
    evaluator(phoner, dataset, memory=memory, certitude=cert_X)
    

    exit()
    


    print("Evaluating...")
    evaluator(wer, "wer", dataset, certitude=cert_X)
    # evaluator(wer, "wer", dataset, certitude=cert_Y)

    evaluator(cer, "cer", dataset, certitude=cert_X)


    print("Evaluated!")

    # semdist
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    # SD_sentence_camembert_large
    model = SentenceTransformer('dangvantuan/sentence-camembert-large')
    # read pickle dicosave
    try:
        with open("datasets/pickle/semdist.pickle", "rb") as file:
            dicosave = pickle.load(file)
    except FileNotFoundError:
        dicosave = dict()
    memory=(model, dicosave)
    evaluator(semdist, "semdist", dataset, memory=memory, certitude=cert_X)
    # evaluator(semdist, dataset, memory=memory, certitude=cert_Y)
    # write pickle dicosave
    with open("datasets/pickle/semdist.pickle", "wb") as file:
        pickle.dump(dicosave, file)