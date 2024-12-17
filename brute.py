import requests
import time
import random
import string
import json
import os
import sys

def save_config(config):
    """
    Saves the configuration to a JSON file.

    Parameters:
        config (dict): The configuration to save.
    """
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def load_config():
    """
    Loads the configuration from a JSON file.

    Returns:
        dict: The loaded configuration, or an empty dict if the file doesn't exist.
    """
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    return {}

def load_credentials(file_path):
    """
    Loads credentials from a file, where each line contains 'username:password'.

    Parameters:
        file_path (str): The path to the credential file.

    Returns:
        list: A list of tuples (username, password).

    Raises:
        FileNotFoundError: If the credential file doesn't exist.
    """
    credentials = []
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split(':')
                if len(parts) == 2:  # Ensure each line has exactly one username and password
                    credentials.append(tuple(parts))
                else:
                    print(f"Invalid line in credentials file: {line.strip()}")
    except FileNotFoundError:
        print(f"Credential file '{file_path}' not found. Exiting.")
        exit(1)

    return credentials

def attempt_login(url, username_field, password_field, username, password):
    """
    Attempts to login using the provided credentials.

    Parameters:
        url (str): The login URL.
        username_field (str): The name of the username field in the form.
        password_field (str): The name of the password field in the form.
        username (str): The username to attempt.
        password (str): The password to attempt.

    Returns:
        response (requests.Response): The response object from the login attempt.
    """
    payload = {username_field: username, password_field: password}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors (4xx, 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during login attempt: {e}")
        return None

def generate_strong_password(length):
    """
    Generates a strong password with at least one lowercase letter, one uppercase letter,
    one digit, and one punctuation character.

    Parameters:
        length (int): The length of the password.

    Returns:
        str: The generated password.

    Raises:
        ValueError: If the length is less than 4.
    """
    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")
    
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    punctuation = random.choice(string.punctuation)
    
    # Fill the rest of the password length with random choices from all character sets
    password = lower + upper + digit + punctuation + \
        ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length - 4))
    
    return ''.join(random.sample(password, len(password)))  # Shuffle to distribute characters

def generate_credentials(count, username_length, password_length):
    """
    Generates a list of random credentials.

    Parameters:
        count (int): The number of credentials to generate.
        username_length (int): The length of the username.
        password_length (int): The length of the password.

    Returns:
        list: A list of tuples (username, password).
    """
    credentials = []
    for _ in range(count):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        password = generate_strong_password(password_length)
        credentials.append((username, password))
    return credentials

def log_attempt(filename, username, password, success):
    """
    Logs the result of a login attempt to a file.

    Parameters:
        filename (str): The file to log the attempts.
        username (str): The username used in the attempt.
        password (str): The password used in the attempt.
        success (bool): Whether the login attempt was successful.
    """
    with open(filename, 'a') as log_file:
        log_file.write(f"{'SUCCESS' if success else 'FAILURE'}: {username}:{password}\n")

def print_progress(current, total):
    """
    Prints a progress bar for the login attempts.

    Parameters:
        current (int): The current attempt number.
        total (int): The total number of attempts.
    """
    percent = (current / total) * 100
    bar = ('#' * int(percent // 2)).ljust(50)
    sys.stdout.write(f"\r[{bar}] {percent:.2f}% ({current}/{total} attempts)")
    sys.stdout.flush()

def main():
    print("Welcome to the Enhanced Authentication Testing Tool!")

    # Load previous configuration if it exists
    config = load_config()

    # User Inputs
    login_url = input("Enter the login URL (e.g., http://example.com/login): ") or config.get("login_url")
    username_field = input("Enter the username field name (e.g., 'username'): ") or config.get("username_field", "username")
    password_field = input("Enter the password field name (e.g., 'password'): ") or config.get("password_field", "password")
    
    credential_file = input("Enter the path to the credential file (e.g., credentials.txt) or 'generate' to create new credentials: ")
    
    if credential_file.lower() == 'generate':
        count = int(input("How many credentials do you want to generate? "))
        username_length = int(input("Enter username length: "))
        password_length = int(input("Enter password length: "))
        credentials = generate_credentials(count, username_length, password_length)
    else:
        credentials = load_credentials(credential_file)

    # Ensure we have credentials
    if not credentials:
        print("No credentials loaded or generated. Exiting.")
        exit(1)

    # Success condition input
    success_indicator = input("Enter a success indicator (e.g., 'Login successful'): ") or config.get("success_indicator", "Login successful")

    # Delay input
    delay_between_attempts = float(input("Enter delay between attempts in seconds (e.g., 1): ")) or config.get("delay", 1.0)

    # Stop on first success option
    stop_on_success = input("Stop on first success? (y/n): ").lower() == 'y'

    # Save configuration for future runs
    save_config({
        "login_url": login_url,
        "username_field": username_field,
        "password_field": password_field,
        "success_indicator": success_indicator,
        "delay": delay_between_attempts
    })

    # Attempt logins
    for index, (username, password) in enumerate(credentials):
        print_progress(index + 1, len(credentials))  # Display progress bar
        response = attempt_login(login_url, username_field, password_field, username, password)

        # Check the response for success
        if response is not None:
            success = success_indicator in response.text
            log_attempt('attempts.log', username, password, success)

            if success:
                print(f"\nSuccessful login with {username}:{password}")
                if stop_on_success:
                    break  # Stop on first success if desired
            else:
                print(f"\nFailed login with {username}:{password}")

            # Randomized delay to avoid rate-limiting detection
            time.sleep(delay_between_attempts + random.uniform(0.5, 1.5))

if __name__ == "__main__":
    main()
