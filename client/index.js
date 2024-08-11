/**
 * This file contains functions for handling user authentication, content loading, and navigation.
 * @file
 */

/**
 * Function to check if the user is authenticated.
 *
 * @function
 * @returns {boolean} Returns true if the user is authenticated, false otherwise.
 */
function isAuthenticated() {
  const token = localStorage.getItem("accessToken");
  return token !== null;
}

/**
 * Function to load the appropriate content based on authentication.
 *
 * @function
 */
function loadContentBasedOnAuthentication() {
  if (isAuthenticated()) {
    // If the user is authenticated, load the user profile
    loadUserProfileContent();
  } else {
    // If not authenticated, load the sign-up form
    loadSignUpForm();
  }
}

/**
 * Function to load face-scan.html content into the right-container.
 *
 * @function
 */
function loadFaceScanContent() {
  // Use fetch to load the content of face-scan.html
  fetch("face-scan.html")
    .then((response) => response.text())
    .then((html) => {
      // Set the HTML content of the right-container to the loaded HTML
      clearRightContainer();
      document.querySelector(".right-container").innerHTML = html;
      loadButtons();
      startWebcamAndShowVideo();
    })
    .catch((error) => {
      console.error("Error loading face-scan.html:", error);
      // Handle the error if the content cannot be loaded
    });
}

/**
 * Function to load user-profile.html content into the right-container.
 *
 * @function
 */
function loadUserProfileContent() {
  fetch("user-profile.html")
    .then((response) => response.text())
    .then((html) => {
      clearRightContainer();
      document.querySelector(".right-container").innerHTML = html;
      fetchAndDisplayUserDetails();
    })
    .catch((error) => {
      console.error("Error loading user-profile.html:", error);
    });
}

/**
 * Function to load the sign-up form into the right-container.
 *
 * @function
 */
function loadSignUpForm() {
  fetch("signup.html")
    .then((response) => response.text())
    .then((html) => {
      clearRightContainer();
      document.querySelector(".right-container").innerHTML = html;
      // Add click event listener for the "Log In" link inside the sign-up form
      const loginLink = document.querySelector('[data-component="login"]');
      loginLink.addEventListener("click", () => {
        clearRightContainer();
        loadLoginForm();
      });
    })
    .catch((error) => {
      console.error("Error loading signup.html:", error);
    });
}

/**
 * Function to load the login form into the right-container.
 *
 * @function
 */
function loadLoginForm() {
  fetch("login.html")
    .then((response) => response.text())
    .then((html) => {
      clearRightContainer();
      document.querySelector(".right-container").innerHTML = html;
      // Add click event listener for the "Register" link inside the login form
      const registerLink = document.querySelector('[data-component="signup"]');
      registerLink.addEventListener("click", () => {
        clearRightContainer();
        loadSignUpForm();
      });
    })
    .catch((error) => {
      console.error("Error loading login.html:", error);
    });
}

/**
 * Add an event listener to call the function when the page loads.
 */
window.addEventListener("load", function () {
  startBackend(); // Call the function on the first load
  // Remove the event listener to prevent it from being called again
  window.removeEventListener("load", arguments.callee);
});

/**
 * Add an event listener to call the function when the page loads.
 */
window.addEventListener("load", loadContentBasedOnAuthentication);

/**
 * Function to clear the content from the right-container.
 *
 * @function
 */
function clearRightContainer() {
  document.querySelector(".right-container").innerHTML = "";
}

/**
 * Function to start the backend.
 *
 * This function makes a GET request to the backend to initiate the necessary actions for starting the backend service.
 *
 * @function
 */
function startBackend() {
  // Show the loading modal before making the request
  showLoadingModal();

  // Make a request to the backend to start it
  fetch(
    "https://biometricauthenticationsystem.onrender.com/user/start-backend",
    {
      method: "GET",
    }
  )
    .then((response) => {
      if (response.status === 200) {
        // Hide the loading modal on success
        hideLoadingModal();
        console.log("Backend started successfully.");
      } else {
        // Show an error message in the loading modal and suggest refreshing the page
        const errorMessage =
          "Failed to start the backend. Please refresh the page and try again.";
        showLoadingError(errorMessage);
        console.error(
          "Failed to start the backend. Status code: " + response.status
        );
      }
    })
    .catch((error) => {
      // Show an error message in the loading modal and suggest refreshing the page
      const errorMessage =
        "Error while starting the backend. Please refresh the page and try again.";
      showLoadingError(errorMessage);
      console.error("Error while starting the backend:", error);
    });
}

/**
 * Function to show the loading modal.
 *
 * This function displays the loading modal on the screen.
 *
 * @function
 */
function showLoadingModal() {
  const loadingModal = document.getElementById("loadingModal");
  loadingModal.style.display = "inline-flex";
}

/**
 * Function to hide the loading modal.
 *
 * This function hides the loading modal from the screen.
 *
 * @function
 */
function hideLoadingModal() {
  const loadingModal = document.getElementById("loadingModal");
  loadingModal.style.display = "none";
}

/**
 * Function to show an error message in the loading modal.
 *
 * This function displays an error message in the loading modal and suggests refreshing the page.
 *
 * @function
 * @param {string} errorMessage - The error message to display.
 */
function showLoadingError(errorMessage) {
  const loadingModal = document.getElementById("loadingModal");
  const loadingContent = loadingModal.querySelector(".loading-content");
  loadingContent.innerHTML = `
    <div class="error-icon">⚠️</div>
    <p>${errorMessage}</p>
  `;
}
