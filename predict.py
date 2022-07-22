from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pyvi import ViTokenizer
import torch

CLASSES = ["POS", "NEG", "NEU"]
model_path = './model/phoBERT_best.pth'
device = '0'

class Predicter(object):
    def __init__(self, model_path, device):
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
        self.model = AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base", num_labels=len(CLASSES))
        self.device = torch.device('cuda:{}'.format(device)) if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device(self.device)))

    def predict(self, texts: list):
        confidences = []  # list độ chính xác của các câu
        classes = []  # list class của các câu
        results = dict()
        for text in texts:
            text = ViTokenizer.tokenize(text)
            inputs = self.tokenizer(text, return_tensors="pt", max_length=256).to(self.device)
            labels = torch.tensor([1]).unsqueeze(0).to(self.device)
            outputs = self.model(**inputs, labels=labels)

            result = torch.max(torch.sigmoid(outputs[1]), 1)
            confidences.append(result[0].cpu().detach().numpy()[0])
            classes.append(result[1].cpu().detach().numpy()[0])

        results['POSITIVE'] = round((classes.count(0) / len(texts))*100, 3)
        results['NEGATIVE'] = round((classes.count(1) / len(texts))*100, 3)
        results['NEUTRAL'] = round((classes.count(2) / len(texts))*100, 3)
        return results

predicter = Predicter(model_path, device)

def deeplearn(texts: list):
    result = dict()
    result['type'] = ''
    result['percent'] = ''

    results = predicter.predict(texts)
    type_ = "POSITIVE"
    percent = results.get("POSITIVE")
    for key in results:
        if results.get(key) > percent:
            type_ = key
            percent = results.get(key)

    result['type'] = type_
    result['percent'] = percent
    return result
