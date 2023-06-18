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


