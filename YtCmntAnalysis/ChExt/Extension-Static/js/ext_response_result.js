chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    var currentURL = tabs[0].url;
    console.log(tabs[0].url);
    var resultContainer = document.getElementById("result-container");
    resultContainer.style.display = "block";

    var youtubeUrl = currentURL; // Get the YouTube URL
    if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
        chrome.runtime.sendMessage({ c_url: youtubeUrl }, function (response) {
            response = response.response;
            // var scores=JSON.stringify(response.Scores)
            // var sentimentColor = sentiment === 'Valid' ? 'springgreen' : 'red';
            // JSON response handler
            console.log("Response Received");
            console.log(response);
            var html = "";
            if (!response.hasOwnProperty("Error")) {
                const icon = response["video_analysis"]["Sentiment_summary"]["sentiment"] === 'Valid' ? "✅" : "❌"
                html += "<h1>" + "Verdict:" + "</h1>";
                html +=
                    "<p>" +
                    response["video_analysis"]["Sentiment_summary"]["sentiment"] + icon +
                    "</p>";
            } else if (response["Error"] === 500) {
                html += "<h1>" + "Verdict:" + "</h1>";
                html +=
                    "<p>" +
                    "Sorry bro, " +
                    "InSufficient Data to make an Analysis 😔" +
                    "</p>";
            } else if (response["Error"] === 403) {
                html += "<h1>" + "Verdict:" + "</h1>";
                html += "<p>" + "Comments are disabled for this video 🙅" + "</p>";
            } else {
                html += "<p>" + "Video not found ⛔" + "</p>";
            }
            resultContainer.innerHTML = html;
        });
    } else {
        resultContainer.innerHTML = "<h2>" + "Enter a valid Youtube URL !" + "</h2>";
    }
});
