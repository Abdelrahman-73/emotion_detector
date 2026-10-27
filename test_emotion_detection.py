"""Unit tests for the emotion detection client."""

import unittest
from unittest.mock import patch

import emotion_detection as implementation
from EmotionDetection.emotion_detection import emotion_detector

API_URL = implementation.API_URL
MODEL_ID = implementation.MODEL_ID


class EmotionDetectorTests(unittest.TestCase):
    """Tests for emotion scoring and API request behavior."""

    @patch("emotion_detection.requests.post")
    def test_five_sentences_return_expected_dominant_emotions(self, mock_post):
        """Identify joy, anger, disgust, sadness, and fear for sample text."""
        examples = (
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        )

        for sentence, dominant_emotion in examples:
            with self.subTest(dominant_emotion=dominant_emotion):
                mock_post.return_value.status_code = 200
                mock_post.return_value.json.return_value = {
                    "emotionPredictions": [
                        {
                            "emotion": {
                                emotion: 0.8 if emotion == dominant_emotion else 0.05
                                for emotion in implementation.EMOTIONS
                            }
                        }
                    ]
                }

                result = emotion_detector(sentence)

                self.assertEqual(result["dominant_emotion"], dominant_emotion)
                self.assertEqual(
                    set(result),
                    {
                        "anger",
                        "disgust",
                        "fear",
                        "joy",
                        "sadness",
                        "dominant_emotion",
                    },
                )

        self.assertEqual(mock_post.call_count, len(examples))

    @patch("emotion_detection.requests.post")
    def test_blank_input_returns_empty_scores_without_api_call(self, mock_post):
        """Return empty emotion values for blank text without calling the API."""
        result = emotion_detector("   ")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(result[emotion] is None for emotion in implementation.EMOTIONS))
        mock_post.assert_not_called()

    @patch("emotion_detection.requests.post")
    def test_bad_api_request_returns_empty_scores(self, mock_post):
        """Return empty emotion values when the API responds with HTTP 400."""
        mock_post.return_value.status_code = 400

        result = emotion_detector("some text")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(result[emotion] is None for emotion in implementation.EMOTIONS))

    @patch("emotion_detection.requests.post")
    def test_server_error_raises_runtime_error(self, mock_post):
        """Raise an error for upstream API failures other than HTTP 400."""
        mock_post.return_value.status_code = 500

        with self.assertRaises(RuntimeError):
            emotion_detector("some text")

    @patch("emotion_detection.requests.post")
    def test_sends_expected_api_request(self, mock_post):
        """Send the required text, model header, and request timeout."""
        mock_post.return_value.status_code = 400

        emotion_detector("I am glad this happened")

        mock_post.assert_called_once_with(
            API_URL,
            json={"raw_document": {"text": "I am glad this happened"}},
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            timeout=10,
        )


if __name__ == "__main__":
    unittest.main()
