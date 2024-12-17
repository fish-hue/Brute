# Enhanced Authentication Testing Tool

This tool is designed for authentication testing by attempting login with a list of credentials against a given login URL. It supports credential generation, logging, and configurable parameters, allowing for repeated use while retaining settings between runs.

## Features

- **Credential Generation**: Generate random credentials with configurable username and password lengths.
- **Persistent Configuration**: Save and load configuration settings (like login URL, success indicator, etc.) between runs using a JSON file.
- **Customizable Login Fields**: Specify the form field names for the username and password fields.
- **Error Handling**: Gracefully handles network errors and displays them in the output.
- **Rate Limiting Avoidance**: Includes randomized delay between login attempts to help avoid detection by rate-limiting systems.
- **Progress Indicator**: Displays a progress bar to show the current status of login attempts.
- **Login Success Detection**: Uses customizable success indicators to determine if a login attempt was successful based on the server's response.
- **Detailed Logging**: Logs all login attempts (both successful and failed) to a file for later review.

---

## Installation

To use this tool, you will need Python 3.x and the `requests` library. Follow the steps below to set it up:

### Prerequisites

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- `requests` library: Install it via `pip` if not already installed.

```bash
pip install requests
```

---

## Usage

### Running the Tool

1. **Clone or download the repository**:
   - If using Git, clone the repository:
     ```bash
     git clone https://github.com/fish-hue/brute.git
     ```

2. **Run the script**:
   - Navigate to the folder where the script is located and run it:
     ```bash
     python brute.py
     ```

3. **Configuration**:
   - The tool will prompt you for the following information:
     - **Login URL**: The URL of the login page (e.g., `http://example.com/login`).
     - **Username Field Name**: The name attribute of the username input field (e.g., `username`).
     - **Password Field Name**: The name attribute of the password input field (e.g., `password`).
     - **Credential File Path or Generate**: Provide a path to a file with credentials in the format `username:password` per line, or type `generate` to create random credentials.
     - **Success Indicator**: The string that the server returns when a login is successful (e.g., "Welcome" or "Login successful").
     - **Delay Between Attempts**: The delay (in seconds) between each login attempt to avoid triggering rate limiting.
     - **Stop on First Success**: Whether to stop after the first successful login attempt.

4. **Progress and Logs**:
   - The tool will display a progress bar during the login attempts.
   - All login attempts will be logged to a file called `attempts.log`.
   - Configuration settings will be saved to `config.json` for use in future runs.

---

## Example Run

```bash
$ python authentication_testing_tool.py

Welcome to the Enhanced Authentication Testing Tool!
Enter the login URL (e.g., http://example.com/login): http://example.com/login
Enter the username field name (e.g., 'username'): username
Enter the password field name (e.g., 'password'): password
Enter the path to the credential file (e.g., credentials.txt) or 'generate' to create new credentials: generate
How many credentials do you want to generate? 10
Enter username length: 8
Enter password length: 12
Enter a success indicator (e.g., 'Login successful'): Welcome
Enter delay between attempts in seconds (e.g., 1): 1
Stop on first success? (y/n): n

[####################] 100.00% (10/10 attempts)
```

---

## Configuration

The configuration (like the login URL, success indicator, etc.) is saved to a file named `config.json`. This allows the tool to automatically load your settings on subsequent runs.

### Example `config.json`

```json
{
  "login_url": "http://example.com/login",
  "username_field": "username",
  "password_field": "password",
  "success_indicator": "Welcome",
  "delay": 1.0
}
```

---

## Logging

The tool logs all login attempts, including whether they were successful or not, to a file called `attempts.log`.

### Example `attempts.log`

```
SUCCESS: user1:password123
FAILURE: user2:password456
SUCCESS: user3:password789
```

---

## Customization

You can modify the following aspects of the script:

- **Username and Password Length**: Adjust how long usernames and passwords are when generating new credentials.
- **Success Indicator**: Change the string used to detect successful logins based on the response text.
- **Headers**: The script includes a default `User-Agent` header, but you can modify or add additional headers as needed.

---

## Troubleshooting

### Common Issues

- **Credential File Issues**: Ensure that your credential file is formatted correctly (`username:password` per line).
- **Timeout Errors**: If you encounter timeouts, try increasing the delay between attempts or check your internet connection.

### Errors in Login Attempts

- The tool will log any errors it encounters during login attempts (e.g., `RequestException` errors) and print them to the console for debugging.

---

## License

This tool is provided as-is and is for educational purposes only. Use it responsibly and within legal boundaries. Always obtain permission before testing any systems.
