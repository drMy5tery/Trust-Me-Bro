$(document).ready(function() {
    $("input[type='url']").on("input", function() {
        this.style.minWidth = ((this.value.length + 1) * 8) + "px";
    });
    $('form').submit(function(event) {
        event.preventDefault();  // Prevent form submission
        startAnimation();
        var youtubeUrl = currentURL // Get the YouTube URL
        if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
            $.ajax({
                type: 'POST',
                url: analysisUrl,
                data: {
                    'csrfmiddlewaretoken': csrfToken,
                    'url': youtubeUrl
                },
                success: function(response) {
                    document.getElementById("result-container").style.display="block";
                    document.getElementById("animationWindow").style.display="none";
                    animationInstance.stop()
                // var scores=JSON.stringify(response.Scores)
                   // var sentimentColor = sentiment === 'Valid' ? 'springgreen' : 'red';
                // JSON response handler
                    console.log("Response Received")
                    console.log(response)
                    var resultContainer = $('#result-container');
                    var html = '<h1>' + response.title + '</h1>';
                    if (!response.hasOwnProperty("Error")) {
                        html += '<p>'+response["video_analysis"]["Sentiment_summary"]["sentiment"]+'</p>';
                    } 
                    else if (response["Error"] === 500) {
                        html+= '<p>'  + "Sorry bro, " + "InSufficient Data to make an Analysis"+'</p>';
                    } 
                    else if (response["Error"] === 403) {
                        html+='<p>'  + "Comments are disabled for this video!"+'</p>';
                    } 
                    else {
                        alert("Video not found");
                    }
                    resultContainer.html(html);
                    },
                    });
            
            
                    
        }
        else {
            alert("Enter a valid Youtube URL!");
        }

    });
            
            
})  