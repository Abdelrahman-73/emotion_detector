let RunSentimentAnalysis = ()=>{
    const textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState !== 4) {
            return;
        }

        const responseElement = document.getElementById("system_response");
        let responseData;
        try {
            responseData = JSON.parse(this.responseText);
        } catch (error) {
            responseElement.textContent = `Request failed (${this.status}).`;
            return;
        }

        if (this.status === 200) {
            responseElement.textContent = JSON.stringify(responseData, null, 2);
        } else {
            responseElement.textContent =
                responseData.error || `Request failed (${this.status}).`;
        }
    };
    xhttp.open(
        "GET",
        `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
        true
    );
    xhttp.send();
}
