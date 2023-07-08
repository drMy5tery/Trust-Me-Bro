var serverhost = 'https://trust-me-bro-my5m7t.vercel.app/';  //hosturl for fetching response 

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // Get the current tab's URL
    var url = serverhost + '/extension/' + '?url=' + encodeURIComponent(request.c_url);

    console.log(url);

    fetch(url)
      .then(response => response.json())
      .then(response => sendResponse({ response }))
      .catch(error => console.log(error));
    return true;  // Will respond asynchronously.
  }
);
