"""Unit tests for the emotion detection client."""

import unittest
from unittest.mock import patch

import emotion_detection

API_URL = emotion_detection.API_URL
MODEL_ID = emotion_detection.MODEL_ID
emotion_detector = emotion_detection.emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Tests for emotion scoring and API request behavior."""

    @patch("emotion_detection.requests.post")
    def test_returns_emotion_scores_and_dominant_emotion(self, mock_post):
        """Return all emotion scores and identify the largest score."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "joy": 0.81,
                        "anger": 0.02,
                        "sadness": 0.04,
                        "fear": 0.03,
                        "disgust": 0.10,
                    }
                }
            ]
        }

        result = emotion_detector("I feel great")

        self.assertEqual(
            result,
            {
                "joy": 0.81,
                "anger": 0.02,
                "sadness": 0.04,
                "fear": 0.03,
                "disgust": 0.10,
                "dominant_emotion": "joy",
            },
        )
        mock_post.assert_called_once_with(
            API_URL,
            json={"raw_document": {"text": "I feel great"}},
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            timeout=10,
        )

    @patch("emotion_detection.requests.post")
    def test_blank_input_raises_value_error(self, _mock_post):
        """Reject whitespace-only input without making an API request."""
        with self.assertRaises(ValueError):
            emotion_detector("   ")

    @patch("emotion_detection.requests.post")
    def test_bad_api_response_raises_runtime_error(self, mock_post):
        """Raise an error when the API responds with a failure status."""
        mock_post.return_value.status_code = 500

        with self.assertRaises(RuntimeError):
            emotion_detector("I feel great")

    @patch("emotion_detection.requests.post")
    def test_bad_request_returns_none_for_all_emotions(self, mock_post):
        """Return empty emotion values when the API reports bad input."""
        mock_post.return_value.status_code = 400
        expected = dict.fromkeys(
            ("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion")
        )

        self.assertEqual(emotion_detector("I feel great"), expected)


if __name__ == "__main__":
    unittest.main()
