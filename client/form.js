/**
 * This file contains functions for handling user sign-up and login processes.
 * @file
 */

/**
 * Function to handle Sign Up button click.
 *
 * @function
 * @param {Event} event - The click event object.
 */
function handleSignUp(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the email and password values
  const emailInput = document.querySelector("#signUpEmail");
  const passwordInput = document.querySelector("#signUpPassword");
  const userNameInput = document.querySelector("#signUpUsername");
  const email = emailInput.value;
  const password = passwordInput.value;
  const username = userNameInput.value;

  // Create a JSON object with the email and password
  const data = {
    email: email,
    password: password,
    username: username,
  };

  // Send a POST request to the signup route
  fetch("https://biometricauthenticationsystem.onrender.com/user/register", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the server response here
      if (data.message === "Registration successful") {
        // Clear input fields upon successful
        userNameInput.value = "";
        emailInput.value = "";
        passwordInput.value = "";
        // Save the JWT token to local storage
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refreshToken", data.refresh_token); // Save the refresh token
        // Load the face-scan.html content into the right-container
        loadFaceScanContent();
      } else {
        // Display the error message
        displayError(data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      // Display the error message
      displayError("An error occurred during registration.");
    });
}

/**
 * Function to handle Log In button click.
 *
 * @function
 * @param {Event} event - The click event object.
 */
function handleLogIn(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the email or username and password values
  const usernameEmailInput = document.querySelector("#logInUsernameEmail");
  const passwordInput = document.querySelector("#logInPassword");
  const usernameEmail = usernameEmailInput.value; // Get email or username
  const password = passwordInput.value;

  // Create a JSON object with the email/username and password
  const data = {
    usernameEmail: usernameEmail, // Send email or username
    password: password,
  };

  // Send a POST request to the login route
  fetch("https://biometricauthenticationsystem.onrender.com/user/login", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the server response here
      if (data.message === "Login successful") {
        // Clear input fields upon successful login
        usernameEmailInput.value = "";
        passwordInput.value = "";
        // Save the JWT token to local storage
        localStorage.setItem("accessToken", data.access_token);
        localStorage.setItem("refreshToken", data.refresh_token); // Save the refresh token
        // Load user-profile.html content into the right-container
        loadUserProfileContent();
      } else {
        // Display the error message
        displayError(data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      // Display the error message
      displayError("An error occurred during login.");
    });
}

/**
 * Function to display an error message.
 *
 * @function
 * @param {string} message - The error message to display.
 */
function displayError(message) {
  const errorSpan = document.querySelector('[data-component="error"]');
  errorSpan.textContent = message;
  errorSpan.style.display = "block";
}
