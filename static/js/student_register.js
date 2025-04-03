document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const videoElement = document.getElementById('video');
    const videoContainer = document.getElementById('video-container');
    const captureBtn = document.getElementById('capture-btn');
    const previewElement = document.getElementById('preview');
    const previewContainer = document.getElementById('preview-container');
    const retakeBtn = document.getElementById('retake-btn');
    const photoInput = document.getElementById('photo');
    const studentForm = document.getElementById('studentForm');
    const submitBtn = document.getElementById('submit-btn');
    
    // Photo source radio buttons
    const cameraOption = document.getElementById('camera-option');
    const uploadOption = document.getElementById('upload-option');
    const cameraSource = document.getElementById('camera-source');
    const uploadSource = document.getElementById('upload-source');
    
    // Upload elements
    const photoUpload = document.getElementById('photo-upload');
    const uploadPreview = document.getElementById('upload-preview');
    const uploadPreviewContainer = document.getElementById('upload-preview-container');
    
    let stream = null;
    let photoTaken = false;
    
    // Initialize camera
    async function initCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'  // Front camera for face photos
                },
                audio: false
            });
            
            videoElement.srcObject = stream;
            
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Error accessing camera. Please make sure you have given camera permissions or try using the upload option.');
            
            // Switch to upload option if camera fails
            uploadOption.checked = true;
            togglePhotoSource();
        }
    }
    
    // Stop camera stream
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }
    
    // Handle photo source switching
    function togglePhotoSource() {
        if (cameraOption.checked) {
            cameraSource.style.display = 'block';
            uploadSource.style.display = 'none';
            initCamera();
        } else {
            cameraSource.style.display = 'none';
            uploadSource.style.display = 'block';
            stopCamera();
        }
    }
    
    cameraOption.addEventListener('change', togglePhotoSource);
    uploadOption.addEventListener('change', togglePhotoSource);
    
    // Capture photo from video
    captureBtn.addEventListener('click', function() {
        if (!videoElement.srcObject) {
            alert('Camera is not available. Please try the upload option.');
            return;
        }
        
        // Create canvas to capture frame
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        
        // Draw video frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        
        // Convert to data URL (image)
        const imageDataUrl = canvas.toDataURL('image/jpeg');
        
        // Show preview
        previewElement.src = imageDataUrl;
        videoContainer.style.display = 'none';
        previewContainer.style.display = 'block';
        
        // Create a Blob and transfer to the file input
        canvas.toBlob(function(blob) {
            const file = new File([blob], 'student_photo.jpg', { type: 'image/jpeg' });
            
            // Create a FileList-like object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            
            // Set the file input's files
            photoInput.files = dataTransfer.files;
            
            photoTaken = true;
        }, 'image/jpeg', 0.9);
    });
    
    // Retake photo
    retakeBtn.addEventListener('click', function() {
        videoContainer.style.display = 'block';
        previewContainer.style.display = 'none';
        photoTaken = false;
        photoInput.value = '';
    });
    
    // Handle file upload
    photoUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            
            // Preview the uploaded image
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadPreview.src = e.target.result;
                uploadPreviewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            // Transfer the file to the hidden input
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            photoInput.files = dataTransfer.files;
        } else {
            uploadPreviewContainer.style.display = 'none';
        }
    });
    
    // Form validation
    studentForm.addEventListener('submit', function(e) {
        const name = document.getElementById('name').value;
        const studentId = document.getElementById('student_id').value;
        const classId = document.getElementById('class_id').value;
        
        if (!name || !studentId || !classId) {
            e.preventDefault();
            alert('Please fill in all required fields (Name, Student ID, and Class).');
            return false;
        }
        
        if (!photoInput.files.length && cameraOption.checked && !photoTaken) {
            e.preventDefault();
            alert('Please take a photo or upload an image of the student.');
            return false;
        }
        
        if (!photoInput.files.length && uploadOption.checked) {
            e.preventDefault();
            alert('Please upload an image of the student.');
            return false;
        }
        
        return true;
    });
    
    // Initialize
    togglePhotoSource();
});
