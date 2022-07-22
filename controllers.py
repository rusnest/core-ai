from predict import *
from svm_predict import *

def evaluate_product(comments: list):
    result = dict()
    result_deep = deeplearn(comments)
    result_machine = machinelearn(comments)

    _type = result_deep.get("type")
    percent = result_deep.get("percent")

    if result_deep.get("type") == result_machine.get("type"):
        if (result_machine.get("percent") > percent):
            percent = result_machine.get("percent")
    elif (result_machine.get("percent") > percent):
        _type = result_machine.get("type")
        percent = result_machine.get("percent")
    result['type'] = _type
    result['percent'] = percent

    return result
