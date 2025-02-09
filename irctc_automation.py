import time
import ast 
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from captca_solver import extract_text_from_base64


class TrainBookingAutomation:
    def __init__(self, user_details, passenger_details):
        """
        Initialize the train booking automation process.
        :param user_details: Dictionary containing user login and booking details.
        :param passenger_details: List of dictionaries containing passenger details.
        """
        self.user_details = user_details
        self.passenger_details = passenger_details
        self.driver = None

    def start_browser(self):
        """
        Starts the browser with appropriate options, including incognito mode.
        """


        # Define optimized Chrome options
        options = Options()
        options.add_argument("--incognito")  # Run in incognito mode
        options.add_argument("--start-maximized")  # Maximize window
        options.add_argument("--disable-dev-shm-usage")  # Prevent crashes on Linux/Docker
        options.add_argument("--disable-extensions")  # Disable extensions for speed
        options.add_argument("--disable-infobars")  # Remove automation warning
        options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logs
        
        # Disable images to load pages faster
        prefs = {"profile.managed_default_content_settings.images": 1}
        options.add_experimental_option("prefs", prefs)
        
        # Define ChromeDriver service (provide the path if necessary)
        service = Service()  # Adjust path if needed
        self.driver = webdriver.Chrome(service=service, options=options)


    def login(self):
        """
        Handles the login process for the IRCTC website.
        """
        try:
            # Open the IRCTC website
            self.driver.get("https://www.irctc.co.in/nget/train-search")

            # Click the LOGIN button
            WebDriverWait(self.driver, 300).until(
               EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Click here to Login in application']"))
            ).click()

            # Enter username
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='userid']"))
            ).send_keys(self.user_details["UserID"])

            # Enter password
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='password']"))
            ).send_keys(self.user_details["Password"])

            # Wait for the Enter key press to indicate CAPTCHA completion
            # Extract the CAPTCHA image using BeautifulSoup and Selenium
            #while a:
            # Locate CAPTCHA image and extract its base64 source
            captcha_image_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'captcha-img'))
            )
            captcha_image_src = captcha_image_element.get_attribute('src')
            # Extract CAPTCHA text (replace with actual extraction logic)
            extracted_text = extract_text_from_base64(captcha_image_src)
            # Locate the CAPTCHA input field and enter the extracted text
            captcha_input_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "captcha"))
            )
            captcha_input_field.clear()
            captcha_input_field.send_keys(extracted_text)
            # Click the 'SIGN IN' button
            WebDriverWait(self.driver, 200).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'SIGN IN')]"))
            ).click()
            
            #try:
            ## Check for login error (invalid CAPTCHA) or successful login
            ## Wait for the loginError element to appear within 5 seconds
            #    login_error_element = WebDriverWait(self.driver, 5).until(
            #        EC.presence_of_element_located((By.CLASS_NAME, "loginError"))
            #    )
            #except TimeoutException:
            #    a= False
            #    print("Login page took too long to load or elements not found.")
            #except NoSuchElementException as e:
            #    a= False
            #    print(f"Error during login: {e}")
            ## Get the text inside the loginError element
            #error_text = login_error_element.text
            #
            #if "Invalid Captcha...." in error_text:
            #    i += 1
            #    print("Login failed: Invalid CAPTCHA entered.")
            #else:
            #    print("Login Successfully")
            #    a = False
            ## Click the 'SIGN IN' button
            #WebDriverWait(self.driver, 20).until(
            #       EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'SIGN IN')]"))).click()
            
        except TimeoutException:
            pass
            print("Login page took too long to load or elements not found.")
        except NoSuchElementException as e:
            pass
            print(f"Error during login: {e}")

    def search_train(self):
        """
        Fills in the train search details.
        """
        try:
            print("section")
            print("Sleep_Time_Over")
            WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-autocomplete='list' and @aria-controls='pr_id_1_list']"))
            ).send_keys(self.user_details["FromStation"])
            WebDriverWait(self.driver, 300).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@aria-autocomplete='list' and @aria-controls='pr_id_2_list']"))
            ).send_keys(self.user_details["ToStation"])
            WebDriverWait(self.driver, 300).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @class='ng-tns-c58-10 ui-inputtext ui-widget ui-state-default ui-corner-all ng-star-inserted']"))
             ).clear()  # Clear the input box
            
            input_field = WebDriverWait(self.driver, 40).until(
               EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @class='ng-tns-c58-10 ui-inputtext ui-widget ui-state-default ui-corner-all ng-star-inserted']"))
            )
            
            # Click and select all text
            input_field.click()
            input_field.send_keys(Keys.CONTROL + "a")  # For selecting all text (works for most browsers)
            input_field.send_keys(Keys.BACKSPACE)  # Delete the selected text

            # Now input the Date
            input_field.send_keys(self.user_details["Date"])

            # Wait for and click the dropdown to open
            dropdown = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'All Classes')]")))
            self.driver.execute_script("arguments[0].click();", dropdown)

            # Wait for and select the "Sleeper (SL)" option
            # Define your variable
            option_value = self.user_details["Class"]  # Replace with the actual key for your variable
            
            # Use the variable in the XPath
            sleeper_option = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[@aria-label='{option_value}']"))
            )
            sleeper_option.click()

            # Wait for and click the dropdown to open
            dropdown = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'GENERAL')]")))
            dropdown.click()

            # Retrieve the value from self.user_details
            aria_label_value = self.user_details["Quota"]  
            
            # Construct and use the XPath dynamically
            general_option = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[@aria-label='{aria_label_value}']"))
            )
            general_option.click()



            # Wait for the "Search" button to be clickable and click it
            search_button = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='search_btn train_Search']")))
            search_button.click()

            # Define your variables
            travel_class = self.user_details["Class"]  # Replace with the key that contains your value, e.g., 'AC 3 Tier (3A)'
            index_number = self.user_details["Class_Index"]  # Replace with your desired index number
            
            # Use the variables in the XPath
            sleeper_button = WebDriverWait(self.driver, 300).until(
                EC.element_to_be_clickable((By.XPATH, f"(//strong[text()='{travel_class}'])[{index_number}]"))
            )
            sleeper_button.click()
            print("Sleeper button clicked")
            # Define your variable for the date
            #date_value = self.user_details["Date_1"]    # Replace this with the actual variable or value you want to use, e.g., self.user_details["TravelDate"]
            #
            ## Use the variable in the XPath
            #date_element = WebDriverWait(self.driver, 40).until(
            #    EC.element_to_be_clickable((By.XPATH, f"//strong[text()='{date_value}']"))
            #)
            #date_element.click()
            print("about to click button")

            # Wait for the button to be clickable and click it
            button = WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable((By.XPATH, f"//strong[text()='{self.user_details['Date_1']}']"))
                )

            button.click()
            # Wait for the "Book Now" button to be clickable and click it
            book_now_button = WebDriverWait(self.driver, 600).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btnDefault train_Search') and text()=' Book Now ']"))
            )
            book_now_button.click()

            print("Train search completed.")
        except TimeoutException:
            print("Train search page took too long to load or elements not found.")
        except ElementNotInteractableException as e:
            print(f"Element not interactable during train search: {e}")

    def fill_passenger_details(self):
        """
        Fills in the passenger details.
        """
        try:
            # Start filling passenger details
            index = 1
            while index <= len(self.passenger_details):
                # Check if the passenger name is empty
                if passenger_details[index]["Passenger Name"] == "":
                    print("Found empty passenger name. Stopping the loop.")
                    break  # Exit loop if an empty name is found
                            
            
                print(f"Processing Passenger {index}: {self.passenger_details[index]}")
            
                # Wait for the name input box
                input_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//input[@aria-controls='pr_id_{6 + index}_list' and @placeholder='Name']")
                    )
                )
                input_box.send_keys(self.passenger_details[index]["Passenger Name"])
            
                # Wait for the age input box
                age_input = self.driver.find_element(By.XPATH, "//input[@formcontrolname='passengerAge' and not(@data-gtm-form-interact-field-id)]")
            
                age_input.clear()
                age_input.send_keys(self.passenger_details[index]["Age"])
            
                # Wait for the gender dropdown
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//select[@formcontrolname='passengerGender' and not(@data-gtm-form-interact-field-id)]")
                    )
                )
                Select(dropdown).select_by_visible_text(self.passenger_details[index]["Gender"])
                if index+1 <= len(self.passenger_details):
                    if passenger_details[index+1]["Passenger Name"] != "":
                        add_passenger_button = WebDriverWait(self.driver, 60).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//span[@class='prenext' and contains(text(), '+ Add Passenger')]")
                            )
                        )
                        add_passenger_button.click()
                
                index += 1  # Move to the next passenger
            
            # Wait for the label to be clickable and then click it
            label = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[text()='Consider for Auto Upgradation.']"))
            )
            label.click()
            

             # Wait for the radiobutton to be visible and clickable
            radio_button = WebDriverWait(self.driver, 10).until(
                 EC.element_to_be_clickable((By.ID, "2"))  # Using ID as a locator
             )
             # Click the radio button
            radio_button.click()
            
            # Wait for the button with the text "Continue" to be clickable
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            ).click()

            # Locate the input field by its ID

            # Wait for the captcha input box to be present
            captcha_box = WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.ID, "captcha"))
            )
            # Scroll to the captcha box
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", captcha_box)

            # Clear the captcha input box and set the value
            captcha_box.clear()  # Clear the existing text (if any


            print("Radio captcha clicked successfully!") 

            time.sleep(10)
            WebDriverWait(self.driver, 120).until(
             EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Continue']"))
            ).click()

            print("Passenger details filled.")
            
            WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))
            ).click()

            
        except NoSuchElementException as e:
            print(f"Error while filling passenger details: {e}")

    def confirm_booking(self):
        """
        Confirms the booking by completing the payment process.
        """
        try:
                  
             # Wait for the input field to be visible
            input_field = WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located((By.ID, "vpaCheck"))
            )
            
            # Input the desired text
            input_field.clear()  # Clear any pre-filled text, if necessary
            input_field.send_keys(self.user_details["UPI_Address"]) # Enter your UPI ID

            pay_button = WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "payment-btn"))
            )
            pay_button.click()

            time.sleep(300) # wait time for downloading ticket
        except NoSuchElementException as e:
            print(f"Error during payment: {e}")

    #def close_browser(self):
    #    """
    #    Closes the browser.
    #    """
    #    if self.driver:
    #        self.driver.quit()

    def book_ticket(self):
        """
        Main method to handle the entire booking process step by step.
        """
        self.start_browser()
        print("Browser started.")
        
        self.login()
        print("Login successful. Proceeding to search for trains...")
        
        self.search_train()
        print("Train search completed. Proceeding to fill passenger details...")
        #time.sleep(180)
        self.fill_passenger_details()
        print("Passenger details filled. Proceeding to confirm booking...")
        
        self.confirm_booking()
        print("Booking process completed.")
           


if __name__ == "__main__":
    #user_details = {
    #    "UserID": "",# Enter your IRCTC username
    #    "Password": "", # Enter your IRCTC password
    #    "FromStation": "",# Enter Boarding Station
    #    "ToStation": "",# Enter Destination Station
    #    "Date": "",# Enter Travel date
    #    "Date_1": "",# Enter Travel date in this format
    #    "Class": "",#AC 3 Tier (3A)  Sleeper (SL) 
    #    "Class_Index": 9, # Manually check train option to select before travel
    #    "Quota": "", # TATKAL GENERAL
    #    "UPI_Address": "", # Enter Upi address
    #    "MobileNo": "1234567890",
    #}
    #passenger Name, age ,gender
    # Dictionary to store passenger details
    #passenger_details = {
    #    1: {"Passenger Name": "Niranjan kumar", "Age": "54", "Gender": "Male"},
    #    2: {"Passenger Name": "", "Age": "", "Gender": ""},
    #    3: {"Passenger Name": "", "Age": "0", "Gender": ""},
    #    4: {"Passenger Name": "", "Age": "0", "Gender": ""},  # Empty name to trigger loop exit
    #}
    
    # Initialize an empty dictionary
    user_details = {}
    
    # Open and read the file
    with open("user_details.txt", "r") as file:
        for line in file:
            # Split key and value using ":"
            if ":" in line:
                key, value = line.strip().split(":", 1)
                user_details[key.strip()] = value.strip()  # Remove leading/trailing spaces

    print(user_details)

    # Initialize an empty dictionary for passenger details
    
    # Open and read the file
    with open("passengers.txt", "r") as file:
        data = file.read()
        # Convert the string into a dictionary
        passenger_details = ast.literal_eval(data)
        

    print(passenger_details)

    booking = TrainBookingAutomation(user_details, passenger_details)
    booking.book_ticket()
