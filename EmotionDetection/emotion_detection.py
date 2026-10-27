"""Compatibility import for the root emotion detection module."""

from emotion_detection import (
    API_URL,
    EMOTIONS,
    MODEL_ID,
    emotion_detector,
)

__all__ = ["API_URL", "EMOTIONS", "MODEL_ID", "emotion_detector"]
