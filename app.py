"""Flask web application for emotion detection."""

from flask import Flask, jsonify, render_template, request

from .emotion_detection import emotion_detector


app = Flask(__name__)


@app.get("/")
def home():
    """Render the application's home page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return emotion scores as JSON."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    try:
        result = emotion_detector(text_to_analyze)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(result)


if __name__ == "__main__":
    app.run()
