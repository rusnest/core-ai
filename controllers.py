from predict import *
from preprocess import preprocess

def evaluate_product(comments: list):
    result = dict()

    comments = preprocess(comments)

    result_deep = deeplearn(comments)

    result['type'] = result_deep.get("type")
    result['percent'] = result_deep.get("percent")

    return result
