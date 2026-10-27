let RunSentimentAnalysis = ()=>{
    const textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState !== 4) {
            return;
        }

        const responseElement = document.getElementById("system_response");
        responseElement.textContent = this.responseText;
    };
    xhttp.open(
        "GET",
        `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
        true
    );
    xhttp.send();
}
