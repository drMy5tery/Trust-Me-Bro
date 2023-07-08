
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            var currentURL=tabs[0].url;
            console.log(tabs[0].url);
            var youtubeUrl = currentURL // Get the YouTube URL
            var resultContainer = document.getElementById("result-container");
            var html = '';
            if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
                chrome.runtime.sendMessage( 
                    {c_url:youtubeUrl},function(response) {
                        response=response.response;
                    // var scores=JSON.stringify(response.Scores)
                       // var sentimentColor = sentiment === 'Valid' ? 'springgreen' : 'red';
                    // JSON response handler
                        console.log("Response Received");
                        console.log(response);
                        if (!response.hasOwnProperty("Error")) {
                            if (response["video_analysis"]["Sentiment_summary"]["sentiment"] === 'InValid')
                            {
                                html += "<h2> Sed! bro  It's an "+response["video_analysis"]["Sentiment_summary"]["sentiment"]+' video</h2>';
                            }
                            else
                            {
                                html += "<h2> Yay! bro  It's a "+response["video_analysis"]["Sentiment_summary"]["sentiment"]+' video</h2>';
                            }
                            
                        } 
                        else if (response["Error"] === 500) {
                            html+= '<h2>'  + "Sorry bro, " + "InSufficient Data to make an Analysis"+'</h2>';
                        } 
                        else if (response["Error"] === 403) {
                            html+='<h2>'  + "Comments are disabled for this video!"+'</h2>';
                        }
                        resultContainer.innerHTML+=html; 
                    });
                
            
                        
            }
            else {
                html+='<h2>'  + "Are you on the right page Bro?"+'</h2>';
            }
            resultContainer.innerHTML+=html;
        });
        