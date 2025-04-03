document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const videoElement = document.getElementById('video');
    const videoContainer = document.getElementById('video-container');
    const captureBtn = document.getElementById('capture-btn');
    const previewElement = document.getElementById('preview');
    const previewContainer = document.getElementById('preview-container');
    const retakeBtn = document.getElementById('retake-btn');
    const classSelect = document.getElementById('class_id');
    const submitBtn = document.getElementById('submit-btn');
    const attendanceForm = document.getElementById('attendanceForm');
    const classroomPhotoInput = document.getElementById('classroom_photo');
    const processingSpinner = document.getElementById('processing-spinner');
    
    // Switch between camera and upload
    const cameraMethod = document.getElementById('camera-method');
    const uploadMethod = document.getElementById('upload-method');
    const cameraContainer = document.getElementById('camera-container');
    const uploadContainer = document.getElementById('upload-container');
    const photoUploadInput = document.getElementById('classroom_photo_upload');
    const uploadPreview = document.getElementById('upload-preview');
    const uploadPreviewContainer = document.getElementById('upload-preview-container');
    
    let stream = null;
    let photoTaken = false;
    
    // Initialize camera
    async function initCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'environment'
                },
                audio: false
            });
            
            videoElement.srcObject = stream;
            videoContainer.style.display = 'block';
            previewContainer.style.display = 'none';
            
            // Reset photo taken flag
            photoTaken = false;
            updateSubmitButton();
            
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Error accessing camera. Please make sure you have given camera permissions or try using the upload option.');
            
            // Switch to upload method if camera fails
            uploadMethod.checked = true;
            toggleMethod();
        }
    }
    
    // Stop camera stream
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }
    
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
            const file = new File([blob], 'classroom_photo.jpg', { type: 'image/jpeg' });
            
            // Create a FileList-like object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            
            // Set the file input's files
            classroomPhotoInput.files = dataTransfer.files;
            
            photoTaken = true;
            updateSubmitButton();
        }, 'image/jpeg', 0.9);
    });
    
    // Retake photo
    retakeBtn.addEventListener('click', function() {
        videoContainer.style.display = 'block';
        previewContainer.style.display = 'none';
        photoTaken = false;
        classroomPhotoInput.value = '';
        updateSubmitButton();
    });
    
    // Handle method switching
    function toggleMethod() {
        if (cameraMethod.checked) {
            cameraContainer.style.display = 'block';
            uploadContainer.style.display = 'none';
            initCamera();
        } else {
            cameraContainer.style.display = 'none';
            uploadContainer.style.display = 'block';
            stopCamera();
            
            // Check if a file is already selected
            if (photoUploadInput.files.length > 0) {
                photoTaken = true;
            } else {
                photoTaken = false;
            }
            updateSubmitButton();
        }
    }
    
    cameraMethod.addEventListener('change', toggleMethod);
    uploadMethod.addEventListener('change', toggleMethod);
    
    // Handle file upload
    photoUploadInput.addEventListener('change', function(e) {
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
            classroomPhotoInput.files = dataTransfer.files;
            
            photoTaken = true;
            updateSubmitButton();
        } else {
            uploadPreviewContainer.style.display = 'none';
            photoTaken = false;
            updateSubmitButton();
        }
    });
    
    // Update submit button state
    function updateSubmitButton() {
        if (classSelect.value && photoTaken) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }
    
    // Handle class selection
    classSelect.addEventListener('change', updateSubmitButton);
    
    // Show loading spinner during form submission
    attendanceForm.addEventListener('submit', function() {
        processingSpinner.style.display = 'flex';
    });
    
    // Initialize
    initCamera();
    updateSubmitButton();
});
