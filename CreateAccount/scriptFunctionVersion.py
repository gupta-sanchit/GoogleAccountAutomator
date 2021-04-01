from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec

URL = 'http://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(URL)  # load the url in the browser

# In the below step we create variables corresponding to the various buttons and text fields that we would be interacting with during the entire process
# We store the xpath of the elements
firstNameXpath = '//*[@id="firstName"]'
lastNameXpath = '//*[@id="lastName"]'
userNameXpath = '//*[@id="username"]'
passwordXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[3]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'
passwordConfirmXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[3]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
firstPageNextXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'
phoneNumberXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div/div[2]/div[1]/div/div[1]/input'
secondPageNextXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'
verificationCodeXpath = '//*[@id="code"]'
verifyXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button/div[2]'

monthDropDownXpath = '//*[@id="month"]'
dayXpath = '//*[@id="day"]'
yearXpath = '//*[@id="year"]'
genderDropDownXpath = '//*[@id="gender"]'
thirdPageNext = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'
skipXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button/div[2]'
agreeXpath = '//*[@id="termsofserviceNext"]/span/span'


def account(inputParams):
    # Load the input params received into variables
    firstName = inputParams['firstName']
    lastName = inputParams['lastName']
    username = inputParams['username']
    password = inputParams['password']
    phoneNumber = inputParams['phoneNumber']
    month = inputParams['month']
    day = inputParams['day']
    year = inputParams['year']
    gender = inputParams['gender']

    # Page ==> 1

    browser.find_element_by_xpath(firstNameXpath).send_keys(firstName)  # First Name Input
    browser.find_element_by_xpath(lastNameXpath).send_keys(lastName)  # Second Name Input

    HandleUsername(username)  # function call to enter username

    browser.find_element_by_xpath(passwordXpath).send_keys(password)  # password input
    browser.find_element_by_xpath(passwordConfirmXpath).send_keys(password)  # re-enter password for confirmation
    browser.find_element_by_xpath(firstPageNextXpath).click()  # clicking the next button to proceed to next page

    # Page ==> 2
    # a time interval is added between pages so that they load fully before we can begin interacting with them

    sleep(10)
    browser.find_element_by_xpath(phoneNumberXpath).send_keys(phoneNumber)  # Phone Number Input
    browser.find_element_by_xpath(secondPageNextXpath).click()  # Click the Next button

    # Page ==> 3 OTP Verification
    # input is taken from the command line to obtain the otp received on the phone number
    verificationCode = input(f"Enter the verification code received on {phoneNumber} ==> ")
    sleep(5)
    browser.find_element_by_xpath(verificationCodeXpath).send_keys(verificationCode)  # entering the verification code
    browser.find_element_by_xpath(verifyXpath).click()  # click on Verify

    # Page ==> 4
    sleep(10)
    browser.find_element_by_xpath(dayXpath).send_keys(day)  # enter Day for Date of Birth
    browser.find_element_by_xpath(yearXpath).send_keys(year)  # enter year for Date of Birth

    # Both Month and enter cannot be entered using text, they are in form of drop-down
    # The drop-down menus are enclosed in select tag therefore, to tackle this, we use selenium's select method here
    # Using select method we can make the selections in the drop-down by simply using the values

    monthOptions = Select(browser.find_element_by_xpath(monthDropDownXpath))
    # The values in the drop-down are in the format of first letter in uppercase & rest in lowercase like January,
    # therefore , to ensure that the month is in required format we use capitalize function which converts only the first letter of string in UpperCase

    monthOptions.select_by_visible_text(month.capitalize())

    genderOptions = Select(browser.find_element_by_xpath(genderDropDownXpath))  # following the same procedure as month for gender selection
    genderOptions.select_by_visible_text(gender.capitalize())

    browser.find_element_by_xpath(thirdPageNext).click()

    # Page 5
    sleep(5)
    browser.find_element_by_xpath(skipXpath).click()  # Skip an optional step

    # Page 6
    sleep(5)
    browser.find_element_by_xpath(agreeXpath).click()  # Terms and conditions agree

    # Explicit Wait
    # element = WebDriverWait(browser, 10, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,StaleElementReferenceException]).until(
    #     ec.presence_of_element_located((By.XPATH, agreeXpath))
    # )

    print("Account Created Successfully !!")


def HandleUsername(username):
    """
    This function is used for entering the username, making sure that the username is available
    In case the username is not available we take the first available username.
    """
    browser.find_element_by_xpath(userNameXpath).send_keys(username)
    browser.find_element_by_xpath("//html").click()
    sleep(1)
    try:
        err = browser.find_element_by_css_selector('.o6cuMc')
        print(err.text)
        print('Using the first available user name')
        sleep(1)
        newUsername = browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[2]/div/ul/li[2]/button')
        print(f"Username used : {newUsername.text}")
        newUsername.click()
    except NoSuchElementException:
        pass


if __name__ == '__main__':
    details = {
        'firstName': 'First',
        'lastName': 'Last',
        'username': 'asffasdasdfasd',
        'password': 'Strong@2021',
        'phoneNumber': '',
        'month': 'January',
        'day': '1',
        'year': '1995',
        'gender': 'male'

    }

    account(inputParams=details)



