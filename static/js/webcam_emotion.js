// webcam_emotion.js
// Real-time face detection with concentration tracking for module completion

let lastConcentrationState = null;
let consecutiveConcentratedFrames = 0;
let consecutiveNotConcentratedFrames = 0;

// Module-wide concentration tracking
let moduleConcentrationData = {
  totalChecks: 0,
  concentratedChecks: 0,
  notConcentratedChecks: 0,
  concentrationPercentage: 0
};

// Global function to test popup (for debugging)
window.testPopup = function() {
  // Set some test data for high concentration
  moduleConcentrationData.totalChecks = 10;
  moduleConcentrationData.concentratedChecks = 8;
  moduleConcentrationData.concentrationPercentage = 80;
  
  showModuleCompletionFeedback();
};

// Test function for low concentration (face detected but poor focus)
window.testLowConcentration = function() {
  moduleConcentrationData.totalChecks = 10;
  moduleConcentrationData.concentratedChecks = 2;
  moduleConcentrationData.concentrationPercentage = 20;
  
  showModuleCompletionFeedback();
};

// Test function for medium concentration
window.testMediumConcentration = function() {
  moduleConcentrationData.totalChecks = 10;
  moduleConcentrationData.concentratedChecks = 5;
  moduleConcentrationData.concentrationPercentage = 50;
  
  showModuleCompletionFeedback();
};

// Test function for NO FACE DETECTED (only "Read Again" button)
window.testNoFaceDetected = function() {
  // Simulate scenario where system checks for face but never finds one
  moduleConcentrationData.totalChecks = 10;  // System made checks
  moduleConcentrationData.concentratedChecks = 0;  // But never found a face
  moduleConcentrationData.notConcentratedChecks = 10;  // All checks failed
  moduleConcentrationData.concentrationPercentage = 0;  // 0% concentration
  
  showModuleCompletionFeedback();
};

// Test function for face detection boxes (Dashboard only)
window.testFaceBoxes = function() {
  const video = document.getElementById('videoInput');
  if (!video) {
    console.log('Video element not found');
    return;
  }
  
  // Test with multiple faces
  const testFaces = [
    { x: 50, y: 50, width: 100, height: 120, confidence: 0.9 },
    { x: 200, y: 80, width: 90, height: 110, confidence: 0.7 }
  ];
  
  drawFaceDetectionBoxes(testFaces, video);
  console.log('Test face boxes drawn');
};

// Face detection box drawing function (Dashboard only)
function drawFaceDetectionBoxes(faceCoordinates, video) {
  const canvas = document.getElementById('faceDetectionCanvas');
  if (!canvas) return; // Only available on dashboard
  
  const ctx = canvas.getContext('2d');
  
  // Clear previous drawings
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  if (!faceCoordinates || faceCoordinates.length === 0) {
    return; // No faces to draw
  }
  
  // Calculate scaling factors between video and canvas
  const videoWidth = video.videoWidth || video.width || 640;
  const videoHeight = video.videoHeight || video.height || 480;
  const scaleX = canvas.width / videoWidth;
  const scaleY = canvas.height / videoHeight;
  
  // Draw boxes for each detected face
  faceCoordinates.forEach((face, index) => {
    // Scale coordinates to canvas size
    const x = face.x * scaleX;
    const y = face.y * scaleY;
    const width = face.width * scaleX;
    const height = face.height * scaleY;
    const confidence = face.confidence || 0.5;
    
    // Choose color based on confidence
    let boxColor, textColor;
    if (confidence > 0.7) {
      boxColor = '#28a745'; // Green for high confidence
      textColor = '#28a745';
    } else if (confidence > 0.5) {
      boxColor = '#ffc107'; // Yellow for medium confidence
      textColor = '#ffc107';
    } else {
      boxColor = '#dc3545'; // Red for low confidence
      textColor = '#dc3545';
    }
    
    // Draw bounding box
    ctx.strokeStyle = boxColor;
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, width, height);
    
    // Draw confidence background
    const labelText = `Face ${index + 1}`;
    const labelWidth = ctx.measureText(labelText).width + 10;
    const labelHeight = 20;
    
    ctx.fillStyle = boxColor;
    ctx.fillRect(x, y - labelHeight, labelWidth, labelHeight);
    
    // Draw text
    ctx.fillStyle = 'white';
    ctx.font = '12px Arial';
    ctx.fillText(labelText, x + 5, y - 5);
    
    // Draw corner indicators for better visibility
    const cornerSize = 15;
    ctx.strokeStyle = boxColor;
    ctx.lineWidth = 4;
    
    // Top-left corner
    ctx.beginPath();
    ctx.moveTo(x, y + cornerSize);
    ctx.lineTo(x, y);
    ctx.lineTo(x + cornerSize, y);
    ctx.stroke();
    
    // Top-right corner
    ctx.beginPath();
    ctx.moveTo(x + width - cornerSize, y);
    ctx.lineTo(x + width, y);
    ctx.lineTo(x + width, y + cornerSize);
    ctx.stroke();
    
    // Bottom-left corner
    ctx.beginPath();
    ctx.moveTo(x, y + height - cornerSize);
    ctx.lineTo(x, y + height);
    ctx.lineTo(x + cornerSize, y + height);
    ctx.stroke();
    
    // Bottom-right corner
    ctx.beginPath();
    ctx.moveTo(x + width - cornerSize, y + height);
    ctx.lineTo(x + width, y + height);
    ctx.lineTo(x + width, y + height - cornerSize);
    ctx.stroke();
  });
}

function startWebcamAndAnalyze(showPopups = false) {
  console.log('startWebcamAndAnalyze called with showPopups:', showPopups);
  
  const video = document.getElementById('videoInput');
  const statusElement = document.getElementById('concentration-status');
  
  if (!video) {
    showDebugMessage('Video element not found', true);
    return;
  }

  showDebugMessage('Video element found, checking camera permissions...');

  // Check camera permissions first
  if (navigator.permissions) {
    navigator.permissions.query({ name: 'camera' }).then(function(result) {
      console.log('Camera permission state:', result.state);
      if (result.state === 'denied') {
        showDebugMessage('Camera permission denied. Please allow camera access in browser settings.', true);
        return;
      }
      proceedWithCameraInit();
    }).catch(err => {
      console.log('Permission query not supported, proceeding anyway:', err);
      proceedWithCameraInit();
    });
  } else {
    console.log('Permissions API not supported, proceeding anyway');
    proceedWithCameraInit();
  }
  
  function proceedWithCameraInit() {
    showDebugMessage('Initializing camera...');

    // Enhanced camera constraints for better detection
    const constraints = {
      video: {
        width: { ideal: 640, max: 1280 },
        height: { ideal: 480, max: 720 },
        frameRate: { ideal: 15, max: 30 },
        facingMode: 'user'
      }
    };

    console.log('Requesting camera access with constraints:', constraints);

    navigator.mediaDevices.getUserMedia(constraints)
      .then(stream => {
        console.log('Camera access granted, stream received:', stream);
        
        // Set video source
        video.srcObject = stream;
        
        showDebugMessage('Camera stream connected, starting video...');
        
        // Start video playback
        const playPromise = video.play();
        
        if (playPromise !== undefined) {
          playPromise.then(() => {
            console.log('Video.play() resolved successfully');
            showDebugMessage('Video playing successfully');
          }).catch(err => {
            console.error('Video.play() failed:', err);
            showDebugMessage(`Video play error: ${err.message}`, true);
          });
        }
        
        // Wait for video to be ready
        video.addEventListener('loadedmetadata', () => {
          console.log(`Camera initialized: ${video.videoWidth}x${video.videoHeight}`);
          
          showDebugMessage(`Camera ready! Resolution: ${video.videoWidth}x${video.videoHeight}`);
          
          // Start analysis with adaptive interval
          let analysisInterval = 2000; // Start with 2 seconds
          
          const analysisLoop = () => {
            console.log('Running analysis loop...');
            analyzeFrame(video, showPopups);
            
            // Adaptive interval based on detection success
            const recentSuccess = moduleConcentrationData.concentratedChecks / Math.max(1, moduleConcentrationData.totalChecks);
            if (recentSuccess > 0.7) {
              analysisInterval = 3000; // Slow down if detection is good
            } else if (recentSuccess < 0.3) {
              analysisInterval = 1500; // Speed up if detection is poor
            } else {
              analysisInterval = 2000; // Default
            }
            
            setTimeout(analysisLoop, analysisInterval);
          };
          
          // Start the analysis loop after a brief delay
          setTimeout(() => {
            console.log('Starting face detection analysis...');
            showDebugMessage('Starting face detection analysis...');
            analysisLoop();
          }, 1000);
        });
        
        video.addEventListener('playing', () => {
          console.log('Video started playing successfully');
          showDebugMessage('Video streaming successfully');
        });
        
        video.addEventListener('error', (e) => {
          console.error('Video error:', e);
          showDebugMessage('Video error - Please refresh page', true);
        });
        
      })
      .catch(err => {
        console.error('Enhanced camera access error:', err);
        console.error('Error name:', err.name);
        console.error('Error message:', err.message);
        
        let errorMessage = '';
        if (err.name === 'NotAllowedError') {
          errorMessage = 'Camera permission denied. Please allow camera access and refresh.';
        } else if (err.name === 'NotFoundError') {
          errorMessage = 'No camera found. Please connect a camera and refresh.';
        } else if (err.name === 'NotSupportedError') {
          errorMessage = 'Camera not supported by browser. Please try Chrome/Firefox.';
        } else if (err.name === 'NotReadableError') {
          errorMessage = 'Camera is being used by another application. Please close other apps using camera.';
        } else {
          errorMessage = `Camera error: ${err.message}. Please refresh page.`;
        }
        
        showDebugMessage(errorMessage, true);
      });
  }
}

// Debug mode toggle
window.toggleDebugMode = function() {
  window.debugMode = !window.debugMode;
  console.log(`Debug mode: ${window.debugMode ? 'ON' : 'OFF'}`);
  
  if (window.debugMode) {
    console.log('Current detection stats:', moduleConcentrationData);
  }
};

// Manual camera restart for debugging
window.restartCamera = function() {
  console.log('Manually restarting camera...');
  const video = document.getElementById('videoInput');
  if (video && video.srcObject) {
    video.srcObject.getTracks().forEach(track => track.stop());
  }
  
  // Reset detection data
  moduleConcentrationData = {
    totalChecks: 0,
    concentratedChecks: 0,
    notConcentratedChecks: 0,
    concentrationPercentage: 0
  };
  
  // Restart camera
  setTimeout(() => {
    const isDashboard = window.location.pathname === '/dashboard' || window.location.pathname === '/';
    startWebcamAndAnalyze(!isDashboard);
  }, 500);
};

// Check camera permissions
window.checkCameraPermissions = function() {
  if (navigator.permissions) {
    navigator.permissions.query({name: 'camera'}).then(function(result) {
      console.log('Camera permission:', result.state);
      if (result.state === 'denied') {
        showDebugMessage('Camera permission is DENIED. Please allow camera access in browser settings.', true);
      } else if (result.state === 'prompt') {
        showDebugMessage('Camera permission will be requested. Please allow access when prompted.');
      } else if (result.state === 'granted') {
        showDebugMessage('Camera permission is GRANTED. Camera should work.');
      }
    }).catch(err => {
      console.log('Permission query not supported:', err);
      showDebugMessage('Permission query not supported by browser. Try camera anyway.');
    });
  } else {
    showDebugMessage('Permissions API not supported by browser. Try camera anyway.');
  }
};

function analyzeFrame(video, showPopups = false) {
  console.log('analyzeFrame called, video ready:', video.readyState >= 2);
  
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth || video.width || 640;
  canvas.height = video.videoHeight || video.height || 480;
  const ctx = canvas.getContext('2d');
  
  try {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  } catch (error) {
    console.error('Error drawing video to canvas:', error);
    return;
  }
  
  // Enhance image quality before sending
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imageData.data;
  
  // Simple brightness/contrast enhancement
  for (let i = 0; i < data.length; i += 4) {
    // Increase contrast slightly
    data[i] = Math.min(255, data[i] * 1.1);     // Red
    data[i + 1] = Math.min(255, data[i + 1] * 1.1); // Green
    data[i + 2] = Math.min(255, data[i + 2] * 1.1); // Blue
  }
  
  ctx.putImageData(imageData, 0, 0);
  const dataUrl = canvas.toDataURL('image/jpeg', 0.8); // Reduced quality for faster processing

  console.log('Sending image to backend for analysis...');

  fetch('/api/emotion', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataUrl })
  })
    .then(response => {
      console.log('Response received from backend:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('Backend response data:', data);
      
      const statusElement = document.getElementById('concentration-status');
      const faceCountElement = document.getElementById('face-count-status');
      
      // Update module concentration tracking
      moduleConcentrationData.totalChecks++;
      
      // Update face count display (dashboard only)
      if (faceCountElement) {
        faceCountElement.innerText = `Faces detected: ${data.face_count || 0}`;
      }
      
      // Draw face detection boxes (dashboard only)
      const isDashboard = window.location.pathname === '/dashboard' || window.location.pathname === '/';
      if (isDashboard && data.face_coordinates) {
        console.log('Drawing face boxes for dashboard:', data.face_coordinates);
        drawFaceDetectionBoxes(data.face_coordinates, video);
      }
      
      if (data.face_detected && data.emotion) {
        // Enhanced status display without confidence
        const method = data.detection_method || 'basic';
        
        statusElement.innerText = `Face detected! Emotion: ${data.emotion}`;
        statusElement.className = 'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        
        console.log(`Face detected! Emotion: ${data.emotion}, Method: ${method}`);
        
        // Enhanced concentration tracking with quality scoring
        if (data.concentration && data.concentration_score > 0.5) {
          consecutiveConcentratedFrames++;
          consecutiveNotConcentratedFrames = 0;
          moduleConcentrationData.concentratedChecks++;
          
          // Show positive feedback for high-quality detection
          if (showPopups && consecutiveConcentratedFrames >= 2 && 
              lastConcentrationState !== 'concentrated' && 
              data.concentration_score > 0.7) {
            showPositiveFeedback();
            lastConcentrationState = 'concentrated';
          }
        } else {
          // Face detected but poor concentration or low quality
          consecutiveNotConcentratedFrames++;
          consecutiveConcentratedFrames = 0;
          moduleConcentrationData.notConcentratedChecks++;
          
          if (showPopups && consecutiveNotConcentratedFrames >= 2 && 
              lastConcentrationState !== 'distracted') {
            showConcentrationReminder();
            lastConcentrationState = 'distracted';
          }
        }
        
      } else {
        statusElement.innerText = 'No face detected - Please position yourself in front of the camera';
        statusElement.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        
        console.log('No face detected in current frame');
        
        consecutiveNotConcentratedFrames++;
        consecutiveConcentratedFrames = 0;
        moduleConcentrationData.notConcentratedChecks++;
        
        // Show concentration reminder for no face detection
        if (showPopups && consecutiveNotConcentratedFrames >= 3 && 
            lastConcentrationState !== 'not_concentrated') {
          showConcentrationReminder();
          lastConcentrationState = 'not_concentrated';
        }
        
        // Clear face detection boxes when no faces detected (dashboard only)
        if (isDashboard) {
          drawFaceDetectionBoxes([], video);
        }
      }
      
      // Calculate enhanced concentration percentage
      moduleConcentrationData.concentrationPercentage = 
        (moduleConcentrationData.concentratedChecks / moduleConcentrationData.totalChecks) * 100;
        
      // Update real-time statistics if debug mode
      if (window.debugMode) {
        console.log(`Detection Stats: Concentrated: ${moduleConcentrationData.concentratedChecks}/${moduleConcentrationData.totalChecks} (${moduleConcentrationData.concentrationPercentage.toFixed(1)}%)`);
      }
        
    })
    .catch(err => {
      console.error('Error analyzing emotion:', err);
      const statusElement = document.getElementById('concentration-status');
      if (statusElement) {
        statusElement.innerText = 'Error analyzing emotion - Please refresh page';
        statusElement.className = 'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
      }
    });
}

function showModuleCompletionFeedback(event) {
  // Prevent immediate navigation
  if (event) {
    event.preventDefault();
  }
  
  const concentrationPercentage = moduleConcentrationData.concentrationPercentage;
  let modalData = {};
  
  // Check if face was actually detected (concentratedChecks > 0 means face was detected at least once)
  const faceDetected = moduleConcentrationData.concentratedChecks > 0;
  
  // If no face detected at all during the module, only allow "Read Again"
  if (!faceDetected || moduleConcentrationData.concentratedChecks === 0) {
    modalData = {
      title: "❌ Face Not Detected",
      message: "No face was detected during this module! Please ensure your face is visible to the camera and read this module again for proper concentration tracking.",
      type: 'danger',
      showMoveNext: false, // Hide "Move to Next" button
      nextHref: event && event.target ? event.target.href : null
    };
  } else if (concentrationPercentage >= 70) {
    // High concentration - Green success popup with both buttons
    const messages = [
      "🎉 Congratulations! You maintained excellent concentration throughout this module!",
      "👏 Outstanding focus! You're ready for the next challenge!",
      "✨ Perfect concentration! You've mastered this module with great focus!",
      "🚀 Excellent work! Your concentration was impressive throughout the learning!"
    ];
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    modalData = {
      title: "✅ Excellent Work!",
      message: randomMessage + ` (${Math.round(concentrationPercentage)}% concentrated)`,
      type: 'success',
      showMoveNext: true, // Show both buttons
      nextHref: event && event.target ? event.target.href : null
    };
    
  } else if (concentrationPercentage >= 40) {
    // Medium concentration - Orange warning popup with both buttons
    modalData = {
      title: "⚠️ Review Recommended",
      message: `Good effort! You were concentrated ${Math.round(concentrationPercentage)}% of the time. Consider reviewing this module again for better understanding.`,
      type: 'warning',
      showMoveNext: true, // Show both buttons
      nextHref: event && event.target ? event.target.href : null
    };
    
  } else {
    // Low concentration - Red error popup with both buttons (but encourage review)
    modalData = {
      title: "❌ Low Concentration Detected",
      message: `You were only concentrated ${Math.round(concentrationPercentage)}% of the time. We strongly recommend reading this module again for better understanding, but the choice is yours.`,
      type: 'danger',
      showMoveNext: true, // Show both buttons but encourage review
      nextHref: event && event.target ? event.target.href : null
    };
  }
  
  showInteractiveModal(modalData);
}

function showInteractiveModal(modalData) {
  // Remove any existing modal
  const existingModal = document.getElementById('concentrationModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // Get button colors and text based on type
  let nextBtnClass, readAgainBtnClass, modalClass;
  switch(modalData.type) {
    case 'success':
      nextBtnClass = 'btn-success';
      readAgainBtnClass = 'btn-outline-success';
      modalClass = 'border-success';
      break;
    case 'warning':
      nextBtnClass = 'btn-warning';
      readAgainBtnClass = 'btn-outline-warning';
      modalClass = 'border-warning';
      break;
    case 'danger':
      nextBtnClass = 'btn-danger';
      readAgainBtnClass = 'btn-outline-danger';
      modalClass = 'border-danger';
      break;
    default:
      nextBtnClass = 'btn-primary';
      readAgainBtnClass = 'btn-outline-primary';
      modalClass = 'border-primary';
  }
  
  // Create buttons HTML based on showMoveNext flag
  let buttonsHtml = '';
  if (modalData.showMoveNext === false) {
    // Only show "Read Again" button when no face detected
    buttonsHtml = `
      <button type="button" class="btn ${readAgainBtnClass} btn-lg" onclick="stayInCurrentModule()" style="min-width: 200px;">
        📖 Read Again
      </button>
    `;
  } else {
    // Show both buttons when face was detected
    buttonsHtml = `
      <button type="button" class="btn ${readAgainBtnClass} btn-lg me-3" onclick="stayInCurrentModule()" style="min-width: 150px;">
        📖 Read Again
      </button>
      <button type="button" class="btn ${nextBtnClass} btn-lg" onclick="moveToNextModule('${modalData.nextHref}')" style="min-width: 150px;">
        ➡️ Move to Next
      </button>
    `;
  }
  
  // Create modal HTML
  const modalHtml = `
    <div class="modal fade" id="concentrationModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content ${modalClass}" style="border-width: 3px;">
          <div class="modal-header">
            <h5 class="modal-title" style="font-size: 1.3rem; font-weight: bold;">${modalData.title}</h5>
          </div>
          <div class="modal-body">
            <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">${modalData.message}</p>
          </div>
          <div class="modal-footer justify-content-center">
            ${buttonsHtml}
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Add modal to document
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  
  // Show modal
  const modal = new bootstrap.Modal(document.getElementById('concentrationModal'));
  modal.show();
}

function moveToNextModule(nextHref) {
  // Close modal
  const modal = bootstrap.Modal.getInstance(document.getElementById('concentrationModal'));
  modal.hide();
  
  // Reset module concentration data for next module
  moduleConcentrationData = {
    totalChecks: 0,
    concentratedChecks: 0,
    notConcentratedChecks: 0,
    concentrationPercentage: 0
  };
  
  // Navigate to next module
  if (nextHref && nextHref !== 'null') {
    window.location.href = nextHref;
  }
}

function stayInCurrentModule() {
  // Close modal and stay on current page
  const modal = bootstrap.Modal.getInstance(document.getElementById('concentrationModal'));
  modal.hide();
  
  // Optional: Reset concentration data to give user a fresh start
  moduleConcentrationData = {
    totalChecks: 0,
    concentratedChecks: 0,
    notConcentratedChecks: 0,
    concentrationPercentage: 0
  };
  
  // Show a small toast message
  showBootstrapToast("📚 Continue reading this module. Your concentration tracking has been reset.", 'info');
}

function showPositiveFeedback() {
  const messages = [
    "🎉 Great! You're concentrated and ready to learn!",
    "👍 Excellent focus! Keep up the good work!",
    "✨ Perfect! You're in the learning zone!",
    "🚀 Amazing concentration! You're doing great!"
  ];
  const randomMessage = messages[Math.floor(Math.random() * messages.length)];
  
  // Create a nice popup with positive feedback
  if (typeof bootstrap !== 'undefined') {
    showBootstrapToast(randomMessage, 'success');
  } else {
    alert(randomMessage);
  }
}

function showConcentrationReminder() {
  const message = "📖 You're not concentrated more. Please try to do it again for better understanding. Position your face in front of the camera to continue learning effectively.";
  
  if (typeof bootstrap !== 'undefined') {
    showBootstrapToast(message, 'warning');
  } else {
    alert(message);
  }
}

function showModuleToast(message, type) {
  const toastContainer = document.getElementById('toast-container') || createToastContainer();
  
  let bgClass, icon, title;
  switch(type) {
    case 'success':
      bgClass = 'bg-success';
      icon = '✅';
      title = 'Module Completed!';
      break;
    case 'warning':
      bgClass = 'bg-warning';
      icon = '⚠️';
      title = 'Review Recommended';
      break;
    case 'danger':
      bgClass = 'bg-danger';
      icon = '❌';
      title = 'Please Review';
      break;
    case 'info':
      bgClass = 'bg-info';
      icon = '📚';
      title = 'Module Completed';
      break;
    default:
      bgClass = 'bg-info';
      icon = 'ℹ️';
      title = 'Module Feedback';
  }
  
  const toastHtml = `
    <div class="toast" role="alert" style="min-width: 400px;">
      <div class="toast-header ${bgClass} text-white">
        <strong class="me-auto">${icon} ${title}</strong>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
      </div>
      <div class="toast-body" style="font-size: 1rem; padding: 1rem;">
        ${message}
      </div>
    </div>
  `;
  
  const toastElement = document.createElement('div');
  toastElement.innerHTML = toastHtml;
  const toast = toastElement.firstElementChild;
  
  toastContainer.appendChild(toast);
  
  const bsToast = new bootstrap.Toast(toast, { delay: 6000 });
  bsToast.show();
  
  toast.addEventListener('hidden.bs.toast', () => {
    toast.remove();
  });
}

function showBootstrapToast(message, type) {
  const toastContainer = document.getElementById('toast-container') || createToastContainer();
  
  const bgClass = type === 'success' ? 'bg-success' : 'bg-warning';
  const icon = type === 'success' ? '✅' : '⚠️';
  
  const toastHtml = `
    <div class="toast" role="alert">
      <div class="toast-header ${bgClass} text-white">
        <strong class="me-auto">${icon} Learning Assistant</strong>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
      </div>
      <div class="toast-body">
        ${message}
      </div>
    </div>
  `;
  
  const toastElement = document.createElement('div');
  toastElement.innerHTML = toastHtml;
  const toast = toastElement.firstElementChild;
  
  toastContainer.appendChild(toast);
  
  const bsToast = new bootstrap.Toast(toast, { delay: 4000 });
  bsToast.show();
  
  toast.addEventListener('hidden.bs.toast', () => {
    toast.remove();
  });
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'toast-container position-fixed top-0 end-0 p-3';
  container.style.zIndex = '1055';
  document.body.appendChild(container);
  return container;
}

// Debug helper function to show messages on page
function showDebugMessage(message, isError = false) {
  console.log(message);
  
  const statusElement = document.getElementById('concentration-status');
  if (statusElement) {
    statusElement.innerText = message;
    statusElement.className = isError ? 
      'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center' :
      'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  showDebugMessage('DOM loaded, initializing webcam...');
  console.log('Current path:', window.location.pathname);
  
  // Dashboard: only show emotion, no popups
  // Course pages: show popups when no face detected
  const isDashboard = window.location.pathname === '/dashboard' || window.location.pathname === '/';
  console.log('Is dashboard:', isDashboard);
  
  // Check if video element exists
  const video = document.getElementById('videoInput');
  console.log('Video element found:', !!video);
  
  if (!video) {
    showDebugMessage('Video element not found on page!', true);
    return;
  }
  
  // Check browser support
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showDebugMessage('Browser does not support camera access', true);
    return;
  }
  
  showDebugMessage('Starting webcam initialization...');
  startWebcamAndAnalyze(!isDashboard); // showPopups = true for course pages, false for dashboard
});
