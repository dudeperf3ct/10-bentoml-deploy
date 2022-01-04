from bento_sentiment_analysis_service import TransformerSentimentService
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast


if __name__ == '__main__':

    ts = TransformerSentimentService()
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    artifact = {"model": model, "tokenizer": tokenizer}
    ts.pack("distilbertModel", artifact)
    saved_path = ts.save()