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
