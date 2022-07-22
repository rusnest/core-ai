import pickle

model_path = "./model/svm.pkl"

classifier = pickle.load(open(model_path, 'rb'))

def machinelearn(texts: list):
    result = dict()
    results = dict()
    classes = [0, 0, 0]  # list class của các câu

    res = classifier.predict(texts)

    for r in res:
        if r == 0:
            classes[0] = classes[0] + 1
        elif r == 1:
            classes[1] = classes[1] + 1
        else:
            classes[2] = classes[2] + 1

    results['POSITIVE'] = round((classes[0] / len(texts))*100, 3)
    results['NEGATIVE'] = round((classes[1] / len(texts))*100, 3)
    results['NEUTRAL'] = round((classes[2] / len(texts))*100, 3)

    _type = "POSITIVE"
    percent = results.get("POSITIVE")
    for key in results:
        if results.get(key) > percent:
            _type = key
            percent = results.get(key)

    result['type'] = _type
    result['percent'] = percent

    return result
