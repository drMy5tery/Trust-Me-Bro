function hasYouTubeVideoId(url) {
  const pattern =
    /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([^\s&?/]+)/;
  const match = url.match(pattern);

  if (match && match[1]) {
    return match[1]; // Returns the video ID
  } else {
    return false; // No video ID found
  }
}

// Function to start the animation
function startAnimation() {
  document.getElementById("result-container").style.display = "none";
  document.getElementById("animationWindow").style.display = "block";
  if (animationInstance) {
    playAnimation(); // If initialized, play the animation
    return;
  }
  var animationWindow = document.querySelector("#animationWindow");
  var animData = {
    wrapper: animationWindow,
    animType: "svg",
    loop: true,
    prerender: true,
    autoplay: true,
    path: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/35984/play_fill_loader.json",
    rendererSettings: {
      // Renderer settings here
      //context: canvasContext, // the canvas context
      scaleMode: "noScale",
      clearCanvas: false,
      progressiveLoad: false, // Boolean, only svg renderer, loads dom elements when needed. Might speed up initialization for large number of elements.
      hideOnTransparent: true, //Boolean, only svg renderer, hides elements when opacity reaches 0 (defaults to true)
    },
  };

  var anim = bodymovin.loadAnimation(animData);
  anim.addEventListener("DOMLoaded", onDOMLoaded);
  anim.setSpeed(1);

  function onDOMLoaded(e) {
    anim.addEventListener("complete", function () {
      // Animation complete event listener
    });
  }
  function playAnimation() {
    if (animationInstance) {
      animationInstance.play();
    }
  }
  animationInstance = anim;
}
$(window).on("load", function () {
  document.getElementById("output").style.visibility = "collapse";

  var link = document.getElementById("input");
  var element = document.getElementById("search");
  link.addEventListener("keypress",handleEvent)
  element.addEventListener("click",handleEvent) 
  function handleEvent(event){
    if (event.key === "Enter" || event.type === "click"){
      {
        const youtubeUrl = link.value;
    
        if (youtubeUrl && hasYouTubeVideoId(youtubeUrl)) {
          startAnimation();
          $.ajax({
            type: "POST",
            url: analysisUrl,
            data: {
              csrfmiddlewaretoken: csrfToken,
              url: youtubeUrl,
            },
            success: function (response) {
              // console.log(response);
              document.getElementById("result-container").style.display = "block";
              document.getElementById("animationWindow").style.display = "none";
              const video_name = document.getElementById("video_name");
              const views = document.getElementById("views");
              const likes = document.getElementById("likes");
              const comments = document.getElementById("comments");
              const video_channel = document.getElementById("video_channel");
              var thumbnail = document.getElementById("thumbnail");
    
              video_name.innerHTML = response["title"];
              views.innerHTML = response["views"];
              likes.innerHTML = response["likes"];
              comments.innerHTML = response["commentcount"];
              video_channel.innerHTML = response["channel_name"];
              thumbnail.src = response["thumbnail"];
    
              const summary_info = document.getElementById("summary_info");
              const summary_text = document.getElementById("summary_text");
    
              if (!response.hasOwnProperty("Error")) {
                summary_info_text = "<span>summary : Yeah bro it's a " +
                response["video_analysis"]["Sentiment_summary"]["sentiment"] +
                " video!! </span>";
                if (response["video_analysis"]["Sentiment_summary"]["sentiment"] === 'invalid') {
                  summary_info_text +=
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="flex-shrink-0 w-5 h-5 text-red-500 dark:text-red-400"> <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /> </svg>';
                } else {
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
                  var score =
                    response.video_analysis.Sentiment_summary.Top_five_comments[
                      i
                    ][1];
    
                  html +=
                    '<li class="flex items-center space-x-3 space-y-1">' +
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="flex-shrink-0 w-5 h-5 text-orange-600 dark:text-orange-500"> <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" /></svg>' +
                    "<span>" +
                    comment +
                    " - Score: " +
                    score +
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
              } else if (response["Error"] === 403) {
                document.getElementById("output").style.visibility = "collapse";
                alert("Comments are disabled for this video!");
              } else {
                document.getElementById("output").style.visibility = "collapse";
                alert("Video not found");
              }
            },
          });
    
          document.getElementById("output").style.visibility = "visible";
        } else {
          alert("No Youtube URL found!");
        }
      };
    }
  }
  var close_element = document.getElementById("close");
  close_element.onclick = function () {
    var input = document.getElementById("input");
    input.value = "";
  };
});
