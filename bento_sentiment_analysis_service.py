from collections import defaultdict
import bentoml

import torch
import torch.nn.functional as F

from bentoml.adapters import JsonInput
from bentoml.frameworks.transformers import TransformersModelArtifact


@bentoml.env(
  requirements_txt_file="./requirements.txt"
)
@bentoml.artifacts([TransformersModelArtifact("distilbertModel")])


class TransformerSentimentService(bentoml.BentoService):
  
    @bentoml.api(input=JsonInput(), batch=False)
    def predict(self, parsed_json):
        src_text = parsed_json.get("text")
        model = self.artifacts.distilbertModel.get("model")
        tokenizer = self.artifacts.distilbertModel.get("tokenizer")
        inputs = tokenizer(src_text, return_tensors="pt")
        input_id = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        with torch.no_grad():
          outputs = model(input_id, attention_mask)
          probs = F.softmax(outputs.logits, dim=1).numpy()[0]
        return self.create_dict(src_text, probs)

    def create_dict(self, text: str, probs: list) -> dict:
        d = defaultdict()
        d["input_text"] = text
        d["pos_label"] = "positive"
        d["pos_score"] = float(probs[1])
        d["neg_label"] = "negative"
        d["neg_score"] = float(probs[0])
        return d


