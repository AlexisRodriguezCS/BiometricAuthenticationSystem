/**
 * This file contains functions for webcam access, face capture, and biometric authentication.
 * @file
 */

/**
 * Function to start the webcam and show the video feed.
 *
 * @function
 */
function startWebcamAndShowVideo() {
  const videoElement = document.getElementById("video-element");
  const webcamSelect = document.getElementById("webcam-select");

  // Enumerate available media devices (webcams)
  navigator.mediaDevices
    .enumerateDevices()
    .then(function (devices) {
      // Filter the devices to get only video input devices (webcams)
      const videoDevices = devices.filter(
        (device) => device.kind === "videoinput"
      );
      // Populate the webcamSelect dropdown with available webcams
      videoDevices.forEach(function (device) {
        const option = document.createElement("option");
        option.value = device.deviceId;
        option.text =
          device.label || `Webcam ${webcamSelect.options.length + 1}`;
        webcamSelect.appendChild(option);
      });
    })
    .catch(function (error) {
      console.error("Error enumerating devices:", error);
    });

  // Get the selected webcam deviceId from the dropdown
  const selectedDeviceId = webcamSelect.value;

  // Get user media with the selected webcam
  navigator.mediaDevices
    .getUserMedia({ video: { deviceId: selectedDeviceId }, audio: false })
    .then(function (stream) {
      videoElement.srcObject = stream;
    })
    .catch(function (error) {
      console.error("Error accessing webcam:", error);
    });
}

/**
 * Function to capture and encode the user's face.
 *
 * @async
 * @function
 * @returns {Promise<Uint8Array|null>} Captured face data or null when no face is detected.
 */
async function captureAndEncodeFace() {
  const videoElement = document.getElementById("video-element");

  // Load face-api.js models
  await faceapi.nets.tinyFaceDetector.loadFromUri("/client/face-api");
  await faceapi.nets.faceLandmark68Net.loadFromUri("/client/face-api");
  await faceapi.nets.faceRecognitionNet.loadFromUri("/client/face-api");

  // Detect faces in the video feed
  const detections = await faceapi
    .detectAllFaces(videoElement, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptors();

  if (detections.length > 0) {
    // Capture and encode the face data from the first detected face
    const faceData = detections[0].descriptor;

    return faceData; // Return the captured face data
  } else {
    console.error("No face detected.");
    return null; // Return null when no face is detected
  }
}

/**
 * Function to set up biometric authentication.
 *
 * @function
 */
function setupBiometricAuthentication() {
  // Disable the button
  const button = document.getElementById("setup-biometrics");
  button.disabled = true;
  button.innerText = "Biometric data capturing...";

  // Capture and encode the user's face
  captureAndEncodeFace()
    .then((capturedFaceData) => {
      if (capturedFaceData) {
        // Send the captured face data to the server for storage
        return fetch(
          "https://biometricauthenticationsystem.onrender.com/store_biometric_data",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ faceData: capturedFaceData }),
          }
        );
      } else {
        throw new Error("No face data captured.");
      }
    })
    .then((response) => {
      if (response.status === 200) {
        button.innerText = "Biometric data captured";
        button.style.color = "#fff";
      } else {
        console.error("Biometric data storage failed.");
        button.innerText = "Capture Failed";
      }
    })
    .catch((error) => {
      console.error("Biometric data capture error:", error);
      button.innerText = "Capture Failed";
    });
}

/**
 * Function to authenticate with biometrics.
 *
 * @function
 */
function authenticateWithBiometrics() {
  const button = document.getElementById("authenticate-biometrics");
  button.classList.remove("btn-danger");
  button.classList.remove("btn-success");
  button.classList.add("btn-primary");
  button.disabled = true;
  button.innerText = "Authenticating...";
  button.style.color = "#fff";
  // Capture the user's face data for authentication
  captureAndEncodeFace()
    .then((capturedFaceData) => {
      if (capturedFaceData) {
        return fetch(
          "https://biometricauthenticationsystem.onrender.com/authenticate_with_biometrics",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ faceData: capturedFaceData }),
          }
        );
      } else {
        throw new Error("No face data captured for authentication.");
      }
    })
    .then((response) => {
      if (response.status === 200) {
        // Biometric authentication successful
        console.log("Biometric authentication successful.");
        // Provide feedback to the user and continue with the login process.
        displaySuccessfulMesssage("Biometric authentication successful.");
        button.classList.add("btn-success");
        button.innerText = "Success!";
        const data = response.json(); // Parse the response as JSON
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refreshToken", data.refresh_token);
        // Wait for 3 seconds and then call loadUserProfileContent
        setTimeout(function () {
          loadUserProfileContent(); // Call your loadUserProfileContent function here
        }, 3000); // 3000 milliseconds = 3 seconds
      } else if (response.status === 401) {
        // Biometric authentication failed
        console.log("Biometric authentication failed.");
        // Provide feedback to the user, e.g., display an error message.
        displayScanError("Biometric authentication failed.");
        button.classList.add("btn-danger");
        button.innerText = "Try again";
        button.disabled = false;
      }
    })
    .catch((error) => {
      // Handle other potential errors.
      console.error("Biometric authentication error:", error);
      displayScanError(error);
      button.classList.add("btn-danger");
      button.innerText = "Try again";
      button.disabled = false;
    });
}

/**
 * Function to load the appropriate content based on authentication.
 *
 * @function
 */
function loadButtons() {
  const userBtns = document.querySelector(".user-btns-container");
  const loginBtns = document.querySelector(".login-btns-container");
  if (isAuthenticated()) {
    // If the user is authenticated, load the user-btns-container
    userBtns.style.display = "flex";
  } else {
    // If not authenticated, load the login-btns-container
    loginBtns.style.display = "flex";
  }
}

/**
 * Function to display an error message.
 *
 * @function
 * @param {string} message - The error message to display.
 */
function displayScanError(message) {
  const errorSpan = document.querySelector('[data-component="feedback"]');
  errorSpan.textContent = message;
  errorSpan.style.display = "block";
}

/**
 * Function to display a successful message.
 *
 * @function
 * @param {string} message - The successful message to display.
 */
function displaySuccessfulMesssage(message) {
  const errorSpan = document.querySelector('[data-component="feedback"]');
  errorSpan.textContent = message;
  errorSpan.style.display = "block";
}
