"""Client for the IBM emotion detection service."""

import requests


API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("joy", "anger", "sadness", "fear", "disgust")
EMPTY_RESULT = {
    "joy": None,
    "anger": None,
    "sadness": None,
    "fear": None,
    "disgust": None,
    "dominant_emotion": None,
}


def emotion_detector(text_to_analyze):
    """Send text to the emotion API and format its emotion scores."""
    if text_to_analyze is None or not str(text_to_analyze).strip():
        return EMPTY_RESULT.copy()

    try:
        response = requests.post(
            API_URL,
            json={"raw_document": {"text": str(text_to_analyze).strip()}},
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            timeout=10,
        )
    except requests.exceptions.RequestException as exc:
        raise RuntimeError("Could not connect to the emotion API.") from exc

    if response.status_code == 400:
        return EMPTY_RESULT.copy()

    if response.status_code != 200:
        raise RuntimeError(f"Emotion API returned status {response.status_code}.")

    try:
        parsed_response = response.json()
    except ValueError as exc:
        raise RuntimeError("Emotion API returned invalid JSON.") from exc

    if not parsed_response.get("emotionPredictions"):
        raise RuntimeError("Emotion API returned no predictions.")

    try:
        scores = parsed_response["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Emotion API returned unexpected data.") from exc

    missing_scores = [emotion for emotion in EMOTIONS if emotion not in scores]
    if missing_scores:
        raise RuntimeError("Emotion API is missing score data.")

    dominant_emotion = max(EMOTIONS, key=scores.get)

    return {
        "joy": scores["joy"],
        "anger": scores["anger"],
        "sadness": scores["sadness"],
        "fear": scores["fear"],
        "disgust": scores["disgust"],
        "dominant_emotion": dominant_emotion,
    }
