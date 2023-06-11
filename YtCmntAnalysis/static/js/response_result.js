$(window).on("load", function () {
  document.getElementById("output").style.visibility = "collapse";

  var link = document.getElementById("input");
  var element = document.getElementById("search");
  // Cache the frequently used DOM elements
  var resultContainer = document.getElementById("result-container");
  var animationWindow = document.getElementById("animationWindow");
  var video_name = document.getElementById("video_name");
  var views = document.getElementById("views");
  var likes = document.getElementById("likes");
  var comments = document.getElementById("comments");
  var video_channel = document.getElementById("video_channel");
  var thumbnail = document.getElementById("thumbnail");
  var summary_info_text = document.getElementById("summary_info");
  var summary_text = document.getElementById("summary_text");

  link.addEventListener("keypress", handleEvent);
  element.addEventListener("click", handleEvent);
  function handleEvent(event) {
    if (event.key === "Enter" || event.type === "click") {
      {
        event.preventDefault();
        startAnimation();
        const youtubeUrl = link.value;

        if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
          $.ajax({
            type: "POST",
            url: analysisUrl,
            data: {
              csrfmiddlewaretoken: csrfToken,
              url: youtubeUrl,
            },
            timeout: 60000,
            success: function (response) {
              // console.log(response);
              resultContainer.style.display = "block";
              animationWindow.style.display = "none";
              animationInstance.stop();

              video_name.innerHTML = response["title"];
              views.innerHTML = response["views"];
              likes.innerHTML = response["likes"];
              comments.innerHTML = response["commentcount"];
              video_channel.innerHTML = response["channel_name"];
              thumbnail.src = response["thumbnail"];

              if (!response.hasOwnProperty("Error")) {
                if (
                  response["video_analysis"]["Sentiment_summary"][
                    "sentiment"
                  ] === "InValid"
                ) {
                  summary_info_text =
                    "<span>Sed!&#128532 bro  It's an " +
                    response["video_analysis"]["Sentiment_summary"][
                      "sentiment"
                    ] +
                    " video!! </span>";
                  summary_info_text +=
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="flex-shrink-0 w-5 h-5 text-red-500 dark:text-red-400"> <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /> </svg>';
                } else {
                  summary_info_text =
                    "<span>Yay!&#128512 bro  It's a " +
                    response["video_analysis"]["Sentiment_summary"][
                      "sentiment"
                    ] +
                    " video!! </span>";
                  summary_info_text +=
                    '<svg class="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>';
                }
                summary_info.innerHTML = summary_info_text;

                html = "<ul> comments with strong reactions : <br/>";
                for (
                  var i = 0;
                  i <
                  response.video_analysis.Sentiment_summary.Top_five_comments
                    .length;
                  i++
                ) {
                  var comment =
                    response.video_analysis.Sentiment_summary.Top_five_comments[
                      i
                    ][0];

                  html +=
                    '<li class="flex items-center space-x-3 space-y-1">' +
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="flex-shrink-0 w-5 h-5 text-orange-600 dark:text-orange-500"> <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" /></svg>' +
                    "<span>" +
                    comment +
                    "</span>" +
                    "</li>";
                }
                html += "</ul>";
                summary_text.innerHTML = html;
              } else if (response["Error"] === 500) {
                summary_info.innerHTML =
                  "Sorry bro, " + "InSufficient Data to make an Analysis";
                (" for this video.");
                summary_text.innerHTML = "";
              } else if (response["Error"] === 504) {
                document.getElementById("output").style.visibility = "collapse";
                alert("Internal API error!");
              } else if (response["Error"] === 403) {
                document.getElementById("output").style.visibility = "collapse";
                alert("Comments are disabled for this video!");
              }else {
                document.getElementById("output").style.visibility = "collapse";
                alert("Video not found");
              }
            },
            error: function (xhr, status, error) {
                // Handle the error
                alert(error);
            }
          });

          document.getElementById("output").style.visibility = "visible";
        } else {
          alert("Enter a valid Youtube URL!");
        }
      }
    }
  }
  var close_element = document.getElementById("close");
  close_element.onclick = function () {
    var input = document.getElementById("input");
    input.value = "";
  };
});
