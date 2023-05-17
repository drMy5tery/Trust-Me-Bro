$(document).ready(function() {
    $("input[type='url']").on("input", function() {
        this.style.minWidth = ((this.value.length + 1) * 8) + "px";
    });
    $('form').submit(function(event) {
        event.preventDefault();  // Prevent form submission
        var url = $('#id_url').val();  // Get the YouTube URL
        $.ajax({
            type: 'POST',
            url: analysisUrl,
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'url': url
            },
            success: function(response) {
                document.getElementById("result-container").style.display="block";
                document.getElementById("animationWindow").style.display="none";
                animationInstance.stop()
               // var scores=JSON.stringify(response.Scores)
                var sentiment = response.Sentiment_summary.sentiment;
                var sentimentColor = sentiment === 'Valid' ? 'springgreen' : 'red';
               // JSON response handler
                console.log("Response Received")
                console.log(response)
                var resultContainer = $('#result-container');
                var html = '<h1>' + response.title + '</h1>';
                html += '<p>Views: ' + response.views + '</p>';
                html += '<p>Likes: ' + response.likes + '</p>';
                html += '<p>Comment Count: ' + response.commentcount + '</p>';
                html += '<p>Like-View Ratio: ' + response.like_view_ratio + '</p>';
                html += '<p>Comment-View Ratio: ' + response.comment_view_ratio + '</p>';

                html += '<h2>Sentiment Summary</h2>';
                html += '<h3 style="color: ' + sentimentColor + ';">Sentiment: ' + sentiment + '</h3>' ;

                html += '<h4>Top Five Comments</h4>';
                html += '<ul>';
                for (var i = 0; i < response.Sentiment_summary.Top_five_comments.length; i++) {
                    var comment = response.Sentiment_summary.Top_five_comments[i][0];
                    var score = response.Sentiment_summary.Top_five_comments[i][1];
                    html += '<li>' + comment + ' - Score: ' + score + '</li>';
                }
                html += '</ul>';

                html += '<h2>Scores</h2>';
                html += '<p>Positive: ' + response.Scores.positive + '</p>';
                html += '<p>Negative: ' + response.Scores.negative + '</p>';
                html += '<p>Neutral: ' + response.Scores.neutral + '</p>';

                resultContainer.html(html);  //result container
            }
        });
    });
});