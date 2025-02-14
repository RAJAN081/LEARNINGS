document.addEventListener("DOMContentLoaded", function () {
    const statusText = document.getElementById("status");
    const videoElement = document.getElementById("videoFeed");
    const toggleButton = document.getElementById("toggleDetection");
    const captureButton = document.getElementById("capture");
    const alertSound = document.getElementById("alertSound");
  
    let detectionEnabled = true;
    let previousStatus = "";
  
    async function updateStatus() {
      if (!detectionEnabled) return;
  
      try {
        const response = await fetch('/face_status');
        const data = await response.json();
        const currentStatus = data.status;
        statusText.innerText = currentStatus;
  
        if (currentStatus === "Face Detected ✅") {
          statusText.style.color = "green";
  
          if (previousStatus !== currentStatus) {
            alertSound.play();
          }
        } else {
          statusText.style.color = "red";
        }
        previousStatus = currentStatus;
      } catch (error) {
        console.error("Error fetching face status:", error);
      }
    }
  
    // Toggle face detection
    toggleButton.addEventListener("click", function () {
      detectionEnabled = !detectionEnabled;
  
      if (detectionEnabled) {
        statusText.innerText = "🔍 Detection Running...";
      } else {
        statusText.innerText = "⏸ Detection Paused";
      }
    });
  
    // Capture image
    captureButton.addEventListener("click", async function () {
      try {
        const response = await fetch('/capture_frame', { method: 'POST' });
        const data = await response.json();
        if (data.image_url) {
          window.location.href = "/download_image";
        } else {
          alert("Capture failed. Try again.");
        }
      } catch (error) {
        console.error("Error capturing image:", error);
      }
    });
  
    setInterval(updateStatus, 1000);
  });
  
