# Train Booking Automation

## Overview
This project automates the process of booking train tickets on the [IRCTC](https://www.irctc.co.in/nget/train-search) website using Python and Selenium WebDriver. It handles user login, train search, filling passenger details, and payment confirmation automatically, with CAPTCHA solving integrated using a custom solver.

## Features
- **Automated login**: Logs in to the IRCTC website using provided credentials.
- **Train search**: Searches for available trains between specified stations, selects the preferred class and quota, and proceeds with the booking.
- **Passenger details**: Automatically fills in passenger information such as name, age, and gender.
- **Captcha solving**: Solves CAPTCHA during the login process using the `captcha_solver` module (ensure it is implemented).
- **Booking confirmation**: Completes the payment process by filling in payment details.

## Requirements
1. Python 3.6+
2. Selenium WebDriver
3. ChromeDriver
4. `captcha_solver.py` (a custom script to solve CAPTCHA, must be implemented separately)
5. Google Chrome (or any compatible browser)

### Install Dependencies
You can install the required libraries using pip:

```bash
pip install selenium 
```
## Setup Instructions
1. **Clone the repository**:
```
git clone https://github.com/yourusername/train-booking-automation.git
cd train-booking-automation
```
2. **Update user and passenger details**:

- Modify the user_details dictionary with your IRCTC account credentials, travel details, and class preferences.
- Update the passenger_details list with the passenger details for booking.

3. **Ensure captcha solver is implemented**:

- Implement or integrate a CAPTCHA solver script to handle CAPTCHA challenges during the login process. The current code uses extract_text_from_base64() from captcha_solver.py.
- Run the script: Execute the script to automate the booking process:
```
python train_booking_automation.py
```
## File Structure
```
train-booking-automation/
│
├── captcha_solver.py           # Custom CAPTCHA solver (must be implemented)
├── train_booking_automation.py # Main automation script
├── README.md                  # Project documentation (this file)
└── requirements.txt            # List of required Python packages
```
## Code Explanation

### 1. `TrainBookingAutomation` Class

This class contains the entire automation logic and is responsible for:

- **Starting the browser**: `start_browser`
- **Logging in to IRCTC**: `login`
- **Searching for trains**: `search_train`
- **Filling passenger details**: `fill_passenger_details`
- **Completing the booking process**: `confirm_booking`
- **Handling the entire booking flow**: `book_ticket`

### 2. Dependencies

- **Selenium WebDriver**: Used to control the browser.
- **CAPTCHA solving logic**: Handled via the `captcha_solver.py` script.

### 3. Steps Performed in the Script

1. **Login**:
   - Navigates to the IRCTC login page.
   - Inputs the username and password.
   - Handles CAPTCHA.

2. **Train Search**:
   - Inputs the station details, class, quota, and date to search for available trains.

3. **Passenger Details**:
   - Fills in the passenger information and proceeds to the next steps.

4. **Booking Confirmation**:
   - Completes the booking by filling in the payment details.

### 4. Error Handling

The script handles multiple exceptions:

- **`TimeoutException`**: Raised when elements are not found within the given time.
- **`NoSuchElementException`**: Raised when an element is missing.
- **`ElementNotInteractableException`**: Raised when an element cannot be interacted with.

