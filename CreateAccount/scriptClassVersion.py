from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


class SignUP:
    def __init__(self):
        self.URL = 'http://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        self.browser.get(self.URL)  # load the url in the browser

        # In the below step we create variables corresponding to the various buttons and text fields that we would be interacting with during the entire process
        # We store the xpath of the elements
        self.firstNameXpath = '//*[@id="firstName"]'
        self.lastNameXpath = '//*[@id="lastName"]'
        self.userNameXpath = '//*[@id="username"]'

        self.passwordXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[3]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'
        self.passwordConfirmXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[3]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'

        self.firstPageNextXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'

        self.phoneNumberXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div/div[2]/div[1]/div/div[1]/input'
        self.secondPageNextXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'

        self.verificationCodeXpath = '//*[@id="code"]'
        self.verifyXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button/div[2]'

        self.monthDropDownXpath = '//*[@id="month"]'
        self.dayXpath = '//*[@id="day"]'
        self.yearXpath = '//*[@id="year"]'

        self.genderDropDownXpath = '//*[@id="gender"]'
        self.thirdPageNext = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'

        self.skipXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button/div[2]'
        self.agreeXpath = '//*[@id="termsofserviceNext"]/span/span'

    def account(self, inputParams):
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

        self.browser.find_element_by_xpath(self.firstNameXpath).send_keys(firstName)  # First Name Input
        self.browser.find_element_by_xpath(self.lastNameXpath).send_keys(lastName)  # Second Name Input
        self.username(username)  # function call to handle username
        self.browser.find_element_by_xpath(self.passwordXpath).send_keys(password)  # password input
        self.browser.find_element_by_xpath(self.passwordConfirmXpath).send_keys(
            password)  # re-enter password for confirmation
        self.browser.find_element_by_xpath(
            self.firstPageNextXpath).click()  # clicking the next button to proceed to next page

        # Page ==> 2
        # a time interval is added between pages so that they load fully before we can begin interacting with them

        sleep(10)
        self.browser.find_element_by_xpath(self.phoneNumberXpath).send_keys(phoneNumber)  # Phone Number Input
        self.browser.find_element_by_xpath(self.secondPageNextXpath).click()  # Click the Next button

        # Page ==> 3 OTP Verification
        # input is taken from the command line to obtain the otp received on the phone number
        verificationCode = input(f"Enter the verification code received on {phoneNumber} ==> ")
        sleep(5)
        self.browser.find_element_by_xpath(self.verificationCodeXpath).send_keys(
            verificationCode)  # entering the verification code
        self.browser.find_element_by_xpath(self.verifyXpath).click()  # click on Verify

        # Page ==> 4
        sleep(10)
        self.browser.find_element_by_xpath(self.dayXpath).send_keys(day)  # enter Day for Date of Birth
        self.browser.find_element_by_xpath(self.yearXpath).send_keys(year)  # enter year for Date of Birth

        # Both Month and enter cannot be entered using text, they are in form of drop-down
        # The drop-down menus are enclosed in select tag therefore, to tackle this, we use selenium's select method here
        # Using select method we can make the selections in the drop-down by simply using the values

        monthOptions = Select(self.browser.find_element_by_xpath(self.monthDropDownXpath))
        # The values in the drop-down are in the format of first letter in uppercase & rest in lowercase like January,
        # therefore , to ensure that the month is in required format we use capitalize function which converts only the first letter of string in UpperCase

        monthOptions.select_by_visible_text(month.capitalize())

        genderOptions = Select(self.browser.find_element_by_xpath(
            self.genderDropDownXpath))  # following the same procedure as month for gender selection
        genderOptions.select_by_visible_text(gender.capitalize())

        self.browser.find_element_by_xpath(self.thirdPageNext).click()

        # Page 5
        sleep(5)
        self.browser.find_element_by_xpath(self.skipXpath).click()  # Skip an optional step

        # Page 6
        sleep(5)
        self.browser.find_element_by_xpath(self.agreeXpath).click()  # Terms and conditions agree

        print("Account Created Successfully !!")

    def username(self, username):
        """
        This function is used for entering the username, making sure that the username is available
        In case the username is not available we take the first available username.
        """
        self.browser.find_element_by_xpath(self.userNameXpath).send_keys(username)
        self.browser.find_element_by_xpath("//html").click()
        sleep(1)
        try:
            err = self.browser.find_element_by_css_selector('.o6cuMc')
            print(err.text)
            print('Using the first available user name')
            sleep(1)
            newUsername = self.browser.find_element_by_xpath(
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
    s = SignUP()
    s.account(inputParams=details)
