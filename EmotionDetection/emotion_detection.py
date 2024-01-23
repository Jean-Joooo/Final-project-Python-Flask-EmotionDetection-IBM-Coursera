import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=myobj, headers=header)

    if response.status_code == 400:
        return {
            'anger': 'None',
            'disgust': 'None',
            'fear': 'None',
            'joy': 'None',
            'sadness': 'None',
            'dominant_emotion': 'None'
        }

    else:
        try:
            formatted_response = json.loads(response.text)
            emotion_predictions = formatted_response['emotionPredictions'][0]['emotion']
            anger_score = emotion_predictions.get('anger', 'None')
            disgust_score = emotion_predictions.get('disgust', 'None')
            fear_score = emotion_predictions.get('fear', 'None')
            joy_score = emotion_predictions.get('joy', 'None')
            sadness_score = emotion_predictions.get('sadness', 'None')
            scores = (anger_score, disgust_score, fear_score, joy_score, sadness_score)
            highest_score = max(scores)
            names = {anger_score: 'anger', disgust_score: 'disgust', fear_score: 'fear',
                     joy_score: 'joy', sadness_score: 'sadness'}
            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': names[highest_score]
            }

        except (json.JSONDecodeError, KeyError, IndexError, ValueError):
            # Handle JSON decoding error or missing keys
            return {
                'anger': 'None',
                'disgust': 'None',
                'fear': 'None',
                'joy': 'None',
                'sadness': 'None',
                'dominant_emotion': 'None'
            }
