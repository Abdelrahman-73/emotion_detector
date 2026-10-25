# Emotion Detection Flask App

From the directory containing the `emotion_detector` package, start the
development server with:

```powershell
py -m emotion_detector.app
```

Then open <http://127.0.0.1:5000/> in a browser. The home page serves the
interface, and `/emotionDetector?textToAnalyze=...` returns the emotion
scores as JSON.

The application requires Flask and requests. If they are not installed, run:

```powershell
py -m pip install Flask requests
```
