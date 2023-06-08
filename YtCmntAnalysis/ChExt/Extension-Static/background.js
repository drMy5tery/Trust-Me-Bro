var serverhost = 'http://127.0.0.1:8000';

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // Get the current tab's URL
    var url = serverhost + '/extension/' + '?url=' + encodeURIComponent(currentURL);

    console.log(url);

    fetch(url)
      .then(response => response.json())
      .then(response => sendResponse({ farewell: response }))
      .catch(error => console.log(error));
    return true;  // Will respond asynchronously.
  }
);
