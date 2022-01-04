from bentoml import load

# get location of saved path: bentoml get TransformerSentimentService:latest --print-location

if __name__ == '__main__':

    saved_path = '/home/dudeperf3ct/bentoml/repository/TransformerSentimentService/20211216191754_AA4F16'
    senti_service = load(saved_path)

    print(senti_service.predict({"text": "i like you!"}))
    
    print(senti_service.predict({"text": "i hate you!"}))

