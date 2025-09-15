// Simple webcam initialization for debugging
// webcam_simple.js

let cameraStream = null;

function initializeCamera() {
    console.log('Initializing camera...');
    
    const video = document.getElementById('videoInput');
    const status = document.getElementById('concentration-status');
    
    if (!video) {
        console.error('Video element not found');
        return;
    }
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        const msg = 'Camera not supported by browser';
        console.error(msg);
        status.innerText = msg;
        status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        return;
    }
    
    status.innerText = 'Requesting camera access...';
    status.className = 'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    
    // Simple constraints
    const constraints = {
        video: {
            width: 640,
            height: 480,
            facingMode: 'user'
        }
    };
    
    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            console.log('Camera access granted!');
            cameraStream = stream;
            
            video.srcObject = stream;
            
            status.innerText = 'Camera connected, starting video...';
            status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
            
            video.onloadedmetadata = () => {
                console.log('Video metadata loaded:', video.videoWidth, 'x', video.videoHeight);
                status.innerText = `Camera ready! (${video.videoWidth}x${video.videoHeight})`;
                status.className = 'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
                
                // Start face detection after 2 seconds
                setTimeout(startFaceDetection, 2000);
            };
            
            video.onerror = (e) => {
                console.error('Video error:', e);
                status.innerText = 'Video playback error';
                status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
            };
        })
        .catch(error => {
            console.error('Camera access error:', error);
            
            let message = 'Camera access failed: ';
            if (error.name === 'NotAllowedError') {
                message += 'Permission denied. Please allow camera access and refresh.';
            } else if (error.name === 'NotFoundError') {
                message += 'No camera found. Please connect a camera.';
            } else if (error.name === 'NotReadableError') {
                message += 'Camera is being used by another app.';
            } else {
                message += error.message;
            }
            
            status.innerText = message;
            status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        });
}

function startFaceDetection() {
    console.log('Starting face detection...');
    
    const status = document.getElementById('concentration-status');
    status.innerText = 'Face detection active - Position your face in front of camera';
    status.className = 'badge bg-primary text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    
    // Simple detection loop
    setInterval(detectFace, 3000);
}

function detectFace() {
    const video = document.getElementById('videoInput');
    const status = document.getElementById('concentration-status');
    
    if (!video || video.readyState < 2) {
        console.log('Video not ready for detection');
        return;
    }
    
    // Create canvas to capture frame
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    
    try {
        ctx.drawImage(video, 0, 0);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
        
        console.log('Sending frame for analysis...');
        
        fetch('/api/emotion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: dataUrl })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Detection result:', data);
            
            if (data.face_detected) {
                status.innerText = `Face detected! Emotion: ${data.emotion || 'unknown'}`;
                status.className = 'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
                
                // Update face count
                const faceCount = document.getElementById('face-count-status');
                if (faceCount) {
                    faceCount.innerText = `Faces detected: ${data.face_count || 1}`;
                }
            } else {
                status.innerText = 'No face detected - Please position yourself in front of camera';
                status.className = 'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
                
                const faceCount = document.getElementById('face-count-status');
                if (faceCount) {
                    faceCount.innerText = 'Faces detected: 0';
                }
            }
        })
        .catch(error => {
            console.error('Detection error:', error);
            status.innerText = 'Face detection error - Check connection';
            status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        });
        
    } catch (error) {
        console.error('Canvas error:', error);
        status.innerText = 'Image capture error';
        status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    }
}

// Manual restart function
window.restartCamera = function() {
    console.log('Manual camera restart...');
    
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    const video = document.getElementById('videoInput');
    if (video) {
        video.srcObject = null;
    }
    
    setTimeout(initializeCamera, 500);
};

// Permission check function
window.checkCameraPermissions = function() {
    const status = document.getElementById('concentration-status');
    
    if (navigator.permissions) {
        navigator.permissions.query({ name: 'camera' }).then(result => {
            status.innerText = `Camera permission: ${result.state}`;
            status.className = result.state === 'granted' ? 
                'badge bg-success text-white py-2 px-3 mb-2 w-100 mt-2 text-center' :
                'badge bg-warning text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        }).catch(err => {
            status.innerText = 'Permission check not supported';
            status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        });
    } else {
        status.innerText = 'Permission API not supported';
        status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    }
};

// Comprehensive system diagnosis
window.diagnoseSystem = function() {
    const status = document.getElementById('concentration-status');
    
    let diagnostics = [];
    
    // Check browser support
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        diagnostics.push('✅ Browser supports camera API');
    } else {
        diagnostics.push('❌ Browser does NOT support camera API');
        status.innerText = 'DIAGNOSIS: Browser does not support camera API. Use Chrome/Firefox/Edge.';
        status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        return;
    }
    
    // Check HTTPS/localhost
    if (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
        diagnostics.push('✅ Secure context (HTTPS/localhost)');
    } else {
        diagnostics.push('⚠️ Non-secure context - may block camera access');
    }
    
    // Check video element
    const video = document.getElementById('videoInput');
    if (video) {
        diagnostics.push('✅ Video element found');
    } else {
        diagnostics.push('❌ Video element NOT found');
    }
    
    // Check for available cameras
    navigator.mediaDevices.enumerateDevices().then(devices => {
        const cameras = devices.filter(device => device.kind === 'videoinput');
        if (cameras.length > 0) {
            diagnostics.push(`✅ ${cameras.length} camera(s) detected`);
        } else {
            diagnostics.push('❌ No cameras detected');
        }
        
        // Display results
        status.innerHTML = diagnostics.join('<br>');
        status.className = 'badge bg-info text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
        
        // Show full report in console
        console.log('=== CAMERA DIAGNOSIS ===');
        console.log(diagnostics.join('\n'));
        console.log('Available cameras:', cameras);
        
    }).catch(err => {
        diagnostics.push(`❌ Cannot enumerate devices: ${err.message}`);
        status.innerHTML = diagnostics.join('<br>');
        status.className = 'badge bg-danger text-white py-2 px-3 mb-2 w-100 mt-2 text-center';
    });
};

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeCamera);
