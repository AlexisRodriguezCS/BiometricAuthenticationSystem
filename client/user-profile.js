/**
 * This file contains functions for handling user logout, account deletion,
 * user details fetching, token expiration checks, and token refreshing.
 * @file
 */

/**
 * Function to handle user logout.
 *
 * @function
 */
function handleLogout() {
  // Make a fetch request to the logout route on the backend
  fetch("https://biometricauthenticationsystem.onrender.com/user/logout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      // Remove both the access token and refresh token from localStorage
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      // Function to show the sign-up form
      loadSignUpForm();
    })
    .catch((error) => {
      console.error("Error:", error);
      // Handle errors if the logout request fails
    });
}

/**
 * Function to handle account deletion.
 *
 * @function
 */
function handleDeleteAccount() {
  const token = localStorage.getItem("accessToken");
  const userEmail = document.getElementById("email").textContent;

  // Check if the access token is expired
  if (isTokenExpired(token)) {
    // Access token is expired, refresh it
    refreshAccessToken();
  }

  if (token) {
    fetch(
      "https://biometricauthenticationsystem.onrender.com/user/delete_account",
      {
        method: "DELETE",
        body: JSON.stringify({ email: userEmail }),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          // Handle cases where account deletion fails
          console.error("Account deletion failed");
        } else {
          // Remove the JWT token from localStorage
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          // Function to show the sign-up form
          loadSignUpForm();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        // Handle errors if the account deletion request fails
      });
  } else {
    // Handle cases where the user is not logged in
    console.error("User not logged in");
  }
}

/**
 * Function to fetch and display user details.
 *
 * @function
 */
function fetchAndDisplayUserDetails() {
  const token = localStorage.getItem("accessToken");
  const usernameElement = document.getElementById("username");
  const emailElement = document.getElementById("email");
  const userIdElement = document.getElementById("user-id");
  const accountCreationDateElement = document.getElementById(
    "account-creation-date"
  );

  // Check if the token is expired
  if (isTokenExpired(token)) {
    // Refresh the access token
    refreshAccessToken();
  }

  if (token) {
    fetch("https://biometricauthenticationsystem.onrender.com/user/details", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          // Handle cases where the user is not logged in or token is invalid
          usernameElement.textContent = "Guest";
          emailElement.textContent = "N/A";
          userIdElement.textContent = "N/A";
          accountCreationDateElement.textContent = "N/A";
          return { message: "User not found" }; // Replace with appropriate error handling
        }
        return response.json();
      })
      .then((data) => {
        if (data.message === "success") {
          // Update the HTML elements with the user's details
          usernameElement.textContent = data.user.username;
          emailElement.textContent = data.user.email;
          userIdElement.textContent = data.user.userId;
          accountCreationDateElement.textContent =
            data.user.accountCreationDate;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        // Handle errors if fetching user details fails
      });
  }
}

/**
 * Function to check if a JWT token is expired.
 *
 * @function
 * @param {string} token - The JWT token to check.
 * @returns {boolean} Returns true if the token is expired, false otherwise.
 */
function isTokenExpired(token) {
  if (!token) {
    return true; // Token is considered expired if it doesn't exist
  }
  const tokenData = JSON.parse(atob(token.split(".")[1])); // Decode the token payload
  const expirationTime = tokenData.exp * 1000; // Convert expiration time to milliseconds
  const currentTime = Date.now();
  return currentTime > expirationTime; // Check if the current time is greater than the expiration time
}

/**
 * Function to refresh the JWT token.
 *
 * @function
 */
function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refreshToken"); // Get the refresh token from localStorage
  if (!refreshToken) {
    // Handle the case where no refresh token is available, prompt the user to log in again
    console.error("No refresh token available. Please log in again.");
    return;
  }

  // Make a request to the server to refresh the access token
  fetch(
    "https://biometricauthenticationsystem.onrender.com/user/refresh_token",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refreshToken }),
    }
  )
    .then((response) => {
      if (!response.ok) {
        // Handle cases where the refresh token request fails, e.g., the refresh token is invalid
        console.error("Refresh token request failed. Please log in again.");
        handleLogout();
        return;
      }
      return response.json();
    })
    .then((data) => {
      if (data.accessToken) {
        // Update the access token in localStorage
        localStorage.setItem("accessToken", data.access_token);
        console.log("Access token refreshed.");
        // You can also update the UI to reflect the refreshed token if needed
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
