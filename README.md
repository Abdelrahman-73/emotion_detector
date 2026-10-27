# Final Project

This project sends text to the IBM Watson NLP emotion service and displays
scores for joy, anger, sadness, fear, and disgust, along with the dominant
emotion. The Python package is named `EmotionDetection`.

From the repository root, start the development server with:

```powershell
py server.py
```

Then open <http://127.0.0.1:5000/> in a browser. The home page serves the
interface, and `/emotionDetector?textToAnalyze=...` returns a formatted
emotion summary. Blank input displays `Invalid text! Please try again!`.

The application requires Flask and requests. If they are not installed, run:

```powershell
py -m pip install Flask requests pylint
```

Run the unit tests from the repository root:

```powershell
py -m unittest discover -s . -p "test_*.py" -v
```

Run static analysis with Pylint:

```powershell
py -m pylint EmotionDetection server.py
```
