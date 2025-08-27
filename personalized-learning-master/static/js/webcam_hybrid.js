// webcam_hybrid.js - Working camera with face detection boxes
let moduleConcentrationData = {
    totalChecks: 0,
    concentratedChecks: 0,
    notConcentratedChecks: 0,
    concentrationPercentage: 0
};

function initializeCamera() {
    const video = document.getElementById('videoInput');
    const status = document.getElementById('concentration-status');
    
    if (!video) {
        console.error('Video element not found');
        return;
    }
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        if (status) {
            status.innerText = 'Camera not supported by browser';
            status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }
        return;
    }
    
    console.log('Initializing camera...');
    
    if (status) {
        status.innerText = 'Requesting camera access...';
        status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    }
    
    navigator.mediaDevices.getUserMedia({ 
        video: { 
            width: { ideal: 640 }, 
            height: { ideal: 480 },
            facingMode: 'user'
        } 
    })
    .then(stream => {
        console.log('Camera access granted');
        video.srcObject = stream;
        
        if (status) {
            status.innerText = 'Camera connected, starting video...';
            status.className = 'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }
        
        video.onloadedmetadata = () => {
            console.log('Video metadata loaded');
            if (status) {
                status.innerText = 'Camera ready! Starting detection...';
                status.className = 'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
            }
            
            // Start emotion analysis
            startEmotionAnalysis();
        };
    })
    .catch(err => {
        console.error('Camera error:', err);
        if (status) {
            let errorMsg = 'Camera error: ';
            if (err.name === 'NotAllowedError') {
                errorMsg = 'Camera permission denied. Please allow camera access.';
            } else if (err.name === 'NotFoundError') {
                errorMsg = 'No camera found. Please connect a camera.';
            } else {
                errorMsg += err.message;
            }
            status.innerText = errorMsg;
            status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }
    });
}

function startEmotionAnalysis() {
    setInterval(() => {
        analyzeFrame();
    }, 2000); // Analyze every 2 seconds
}

function analyzeFrame() {
    const video = document.getElementById('videoInput');
    if (!video || video.readyState < 2) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    
    try {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        
        fetch('/api/emotion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: dataUrl })
        })
        .then(response => response.json())
        .then(data => {
            updateUI(data, video);
        })
        .catch(err => {
            console.error('Analysis error:', err);
        });
    } catch (error) {
        console.error('Canvas error:', error);
    }
}

function updateUI(data, video) {
    const status = document.getElementById('concentration-status');
    const faceCount = document.getElementById('face-count-status');
    
    // Update face count
    if (faceCount) {
        faceCount.innerText = `Faces detected: ${data.face_count || 0}`;
    }
    
    // Update concentration data
    moduleConcentrationData.totalChecks++;
    
    if (data.face_detected) {
        moduleConcentrationData.concentratedChecks++;
        if (status) {
            status.innerText = `Face detected! Emotion: ${data.emotion || 'unknown'}`;
            status.className = 'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }
    } else {
        moduleConcentrationData.notConcentratedChecks++;
        if (status) {
            status.innerText = 'No face detected - Please position yourself in front of camera';
            status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }
    }
    
    // Draw face detection boxes (dashboard only)
    const isDashboard = window.location.pathname === '/dashboard' || window.location.pathname === '/';
    if (isDashboard && data.face_coordinates) {
        drawFaceDetectionBoxes(data.face_coordinates, video);
    }
    
    // Update concentration percentage
    moduleConcentrationData.concentrationPercentage = 
        (moduleConcentrationData.concentratedChecks / moduleConcentrationData.totalChecks) * 100;
}

// Face detection box drawing function
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
        let boxColor;
        if (confidence > 0.7) {
            boxColor = '#28a745'; // Green for high confidence
        } else if (confidence > 0.5) {
            boxColor = '#ffc107'; // Yellow for medium confidence
        } else {
            boxColor = '#dc3545'; // Red for low confidence
        }
        
        // Draw bounding box
        ctx.strokeStyle = boxColor;
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, width, height);
        
        // Draw label background
        const labelText = `Face`;  // Simple label since we only detect one face
        const labelWidth = ctx.measureText(labelText).width + 10;
        const labelHeight = 20;
        
        ctx.fillStyle = boxColor;
        ctx.fillRect(x, y - labelHeight, labelWidth, labelHeight);
        
        // Draw text
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.fillText(labelText, x + 5, y - 5);
        
        // Draw corner indicators
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

// Test functions for debugging
window.restartCamera = function() {
    console.log('Restarting camera...');
    const video = document.getElementById('videoInput');
    if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
    
    setTimeout(() => {
        initializeCamera();
    }, 500);
};

window.checkCameraPermissions = function() {
    if (navigator.permissions) {
        navigator.permissions.query({name: 'camera'}).then(function(result) {
            const status = document.getElementById('concentration-status');
            if (status) {
                status.innerText = `Camera permission: ${result.state}`;
                status.className = result.state === 'granted' ? 
                    'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center' :
                    'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
            }
        });
    }
};

window.testFaceBoxes = function() {
    const video = document.getElementById('videoInput');
    if (!video) return;
    
    // Test with sample face data
    const testFaces = [
        { x: 50, y: 50, width: 100, height: 120, confidence: 0.9 },
        { x: 200, y: 80, width: 90, height: 110, confidence: 0.7 }
    ];
    
    drawFaceDetectionBoxes(testFaces, video);
    console.log('Test face boxes drawn');
};

window.diagnoseSystem = function() {
    const status = document.getElementById('concentration-status');
    
    let diagnostics = [];
    
    // Check browser support
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        diagnostics.push('✅ Browser supports camera API');
    } else {
        diagnostics.push('❌ Browser does NOT support camera API');
    }
    
    // Check video element
    const video = document.getElementById('videoInput');
    if (video) {
        diagnostics.push('✅ Video element found');
    } else {
        diagnostics.push('❌ Video element NOT found');
    }
    
    // Check canvas element
    const canvas = document.getElementById('faceDetectionCanvas');
    if (canvas) {
        diagnostics.push('✅ Canvas element found');
    } else {
        diagnostics.push('❌ Canvas element NOT found');
    }
    
    if (status) {
        status.innerHTML = diagnostics.join('<br>');
        status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    }
    
    console.log('=== SYSTEM DIAGNOSIS ===');
    console.log(diagnostics.join('\n'));
};

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeCamera);
