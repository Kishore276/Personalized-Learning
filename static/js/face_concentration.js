// face_concentration.js
// Uses face-api.js for face and emotion detection
// Shows pop-up if user is not concentrating

// Load models from CDN or local
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/models')
]).then(startVideo);

function startVideo() {
  const video = document.getElementById('videoInput');
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    });
}

const concentrationEmotions = ['neutral', 'happy'];

function showConcentrationPopup() {
  alert('You are not concentrating. Please make sure to concentrate or you can take a cup of coffee and come back within 5 minutes.');
}

document.addEventListener('DOMContentLoaded', () => {
  const video = document.createElement('video');
  video.id = 'videoInput';
  video.autoplay = true;
  video.style.display = 'none'; // Hide video element
  document.body.appendChild(video);

  video.addEventListener('play', () => {
    const interval = setInterval(async () => {
      const detections = await faceapi.detectSingleFace(video, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();
      if (detections && detections.expressions) {
        const sorted = Object.entries(detections.expressions).sort((a, b) => b[1] - a[1]);
        const topEmotion = sorted[0][0];
        if (!concentrationEmotions.includes(topEmotion)) {
          showConcentrationPopup();
          clearInterval(interval); // Stop further checks after popup
        }
      }
    }, 5000); // Check every 5 seconds
  });
});
