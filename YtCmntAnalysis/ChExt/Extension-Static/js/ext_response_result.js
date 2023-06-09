
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            var currentURL=tabs[0].url;
            console.log(tabs[0].url);
            var youtubeUrl = currentURL // Get the YouTube URL
            if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
                chrome.runtime.sendMessage( 
                    {c_url:youtubeUrl},function(response) {
                        response=response.response;
                        document.getElementById("result-container").style.display="block";
                    // var scores=JSON.stringify(response.Scores)
                       // var sentimentColor = sentiment === 'Valid' ? 'springgreen' : 'red';
                    // JSON response handler
                        console.log("Response Received");
                        console.log(response);
                        var resultContainer = document.getElementById("result-container");
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
                        resultContainer.innerHTML+=html;
                    });
                
            
                        
            }
            else {
                alert("Enter a valid Youtube URL!");
            }
        });
        