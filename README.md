<a name="readme-top"></a>

<p align="center">
  <img src="https://raw.githubusercontent.com/AlexisRodriguezCS/BiometricAuthenticationSystem/main/images/biometric.jpg" alt="Grid" style="display:block;margin:auto;" height="500">
</p>
<h1 align="center">Biometric Authentication System</h1>

<!-- TABLE OF CONTENTS -->
<p align="center">
  <a href="#about">About The Project</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#contact">Contact</a> •
  <a href="#credit">Credit</a>
</p>

<!-- ABOUT THE PROJECT -->

<a name="about"></a>

## About The Project

**Welcome to the Biometric Authentication System project!** This full-stack web application combines HTML, CSS, and JavaScript on the front-end, featuring the remarkable [face-api.js](https://github.com/justadudewhohacks/face-api.js) library for advanced facial recognition. On the back-end, we've harnessed the power of Python, Flask, PostgreSQL, JWT (JSON Web Tokens), and bcrypt to craft a robust and secure authentication system.

### Overview

This project's primary goal is to deliver a secure and user-friendly authentication system that harmoniously integrates traditional username and password credentials with state-of-the-art biometric technology. Users can easily register by providing their email, username, and a password. For those equipped with a webcam, we provide an option to employ their facial features as a biometric identifier. The magic of face recognition is enabled through the integration of the face-api.js library.

Once registered, users can conveniently log in using either their email/username and password or their previously scanned face. We've also implemented an account deletion feature, which removes all associated data.

This project is designed for demonstration purposes, and we do not engage in the sale or sharing of biometric data.

### Hosting

The frontend of the application is hosted on Netlify, while the backend is deployed on Render.
**You can access the live website at this link:
<a href="https://biometricauthenticationsystem.netlify.app/" target="_blank">Biometric Authentication System</a>**

<mark>**Please note that the backend, hosted on Render's free tier for demonstration purposes, may take a minute or two to start up. <ins>However, once the backend is up and running, the website will function as intended.**</ins></mark>

### Key Technologies Used

- Python: The primary programming language used to develop the Flask backend.
- Flask: A micro web framework for building the backend of the application.
- SQLAlchemy: Used for database operations to interact with the PostgreSQL database.
- PostgreSQL: A powerful open-source relational database management system.
- JWT (JSON Web Tokens): Utilized for user authentication and token-based security.
- bcrypt: A library for hashing passwords securely.
- Face-api.js: A JavaScript library for face detection and recognition.
- Webcam API: For accessing and capturing video from the user's webcam.
- HTML and CSS: For creating the user interface of the website.
- JavaScript: For client-side scripting to handle user interactions.
- Fetch API: Used for making asynchronous requests to the backend.
- CORS (Cross-Origin Resource Sharing): Used for enabling cross-origin requests.
- Bootstrap MDB (Material Design for Bootstrap): A framework for building responsive and visually appealing user interfaces.
- Google Fonts: For custom fonts and typography on the website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

<a name="project-structure"></a>

## Project Structure

### Front-End

The front-end of the application is organized into the following directories:

- `\client`: Contains the main client-side web application code.
  - `\face-api`: Houses JavaScript code for face recognition using TensorFlow.js.
  - `\mdb`: Utilizes Material Design for Bootstrap 5 and Vanilla JavaScript for creating the user interface.

### Components

| File              | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| face-scan.html    | A page to capture biometric data using a webcam.                   |
| index.html        | The main page with left and right containers for content.          |
| login.html        | A log-in form for returning users.                                 |
| signup.html       | A sign-up form for registering new users.                          |
| user-profile.html | A user profile page displaying details.                            |
| face-scan.css     | Styles for the face-scan.html page.                                |
| index.css         | Styles for the main index.html page.                               |
| user-profile.css  | Styles for the user-profile.html page.                             |
| face-scan.js      | Handles webcam access and biometric authentication.                |
| index.js          | Manages user authentication, content loading, and backend startup. |
| form.js           | Manages user registration and login processes.                     |
| user-profile.js   | Manages profile details, and token handling.                       |

### Back-End

The back-end of the application is organized into the following directories:

- `server` Folder:
  - `database:` Database configurations and migration scripts.
  - `migrations`: Database schema evolution scripts.
  - `models`: Database model definitions.
  - `routes`: API route definitions and controllers.
  - `app.py`: Main Flask application configuration.
  - `requirements.txt`: Project dependencies list.

### Components

| File             | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| db.py            | Database Configuration using Flask-SQLAlchemy.                     |
| models/user.py   | User Model for representing registered users.                      |
| routes/user.py   | User Routes for various user-related functionality.                |
| app.py           | Flask Application Configuration with initialized extensions.       |
| requirements.txt | List of Python packages and versions required for the application. |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

<a name="getting-started"></a>

## Getting Started

To access the online hosted version of the project, click [here](https://biometricauthenticationsystem.netlify.app/).

To set up a project locally, follow these simple steps.

### Prerequisites

_Software I used to run the program._

- [Visusal Studio Code](https://code.visualstudio.com/)

- [Python](https://www.python.org/downloads/)

- [PostgreSQL](https://www.postgresql.org/download/)

- [pgAdmin 4](https://www.pgadmin.org/download/pgadmin-4-windows/)

- [Git](https://git-scm.com/)

- [Postman](https://www.postman.com/downloads/)

- [Live Sever](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

### Installation

_Here's how to install and set up the program._

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/AlexisRodriguezCS/BiometricAuthenticationSystem.git

# Go into the repository
$ cd BiometricAuthenticationSystem

# Right-click on the HTML file (index.html)
$ Open with Live Server.

# Go into the repository
$ cd server

# Create a virtual environment
$ python -m venv venv

# Activate the virtual environment
$ venv\Scripts\activate

# Install the Python packages listed in a requirements.txt
$ pip install -r requirements.txt

# Run your Flask app
$ python app.py
```

```bash
# Flask app will start and should display something like this:
$ * Running on http://127.0.0.1:5000/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

<a name="usage"></a>

## Usage

1. Visit the [Biometric Authentication System Website](https://biometricauthenticationsystem.netlify.app/).
2. Wait for the backend to start. This may take a minute or two, so please be patient.

### New Users

1. On the website, you can create an account by following these steps:
   - Click on "Register" link.
   - Provide your email, a username, and a secure password.
2. Grant the necessary permissions for web access in your browser.
3. Ensure your webcam is active and select the correct camera source.
4. Follow the on-screen instructions to scan your face accurately.
5. Click the "Start Scan" button to initiate the face scan.
6. Once the face scan is completed, you can use it for authentication.

### Returning Users

1. If you're a returning user, go to the login form on the website.
2. Provide either your email or username, along with your password to log in.
3. Alternatively, if you have previously scanned your face, you can use it for authentication.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

<a name="contact"></a>

## Contact

Alexis Rodriguez - [LinkedIn](https://www.linkedin.com/in/alexisrodriguezcs/) - alexisrodriguezdev@gmail.com

Project Link: [https://github.com/AlexisRodriguezCS/BiometricAuthenticationSystem.git](https://github.com/AlexisRodriguezCS/BiometricAuthenticationSystem.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="credit"></a>

## Credits

[face-api.js](https://github.com/justadudewhohacks/face-api.js) - The face recognition library used in this project.

[Material Design for Bootstrap 5](https://mdbootstrap.com/) - Framework for building responsive and visually appealing user interfaces.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
