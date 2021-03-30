from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


class SignUP:
    def __init__(self):
        self.URL = 'http://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        self.browser.get(self.URL)

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

        self.browser.find_element_by_xpath(self.firstNameXpath).send_keys(firstName)
        self.browser.find_element_by_xpath(self.lastNameXpath).send_keys(lastName)
        self.username(username)
        self.browser.find_element_by_xpath(self.passwordXpath).send_keys(password)
        self.browser.find_element_by_xpath(self.passwordConfirmXpath).send_keys(password)
        self.browser.find_element_by_xpath(self.firstPageNextXpath).click()

        # Page ==> 2

        sleep(10)
        self.browser.find_element_by_xpath(self.phoneNumberXpath).send_keys(phoneNumber)
        self.browser.find_element_by_xpath(self.secondPageNextXpath).click()

        # Page ==> 3 OTP Verification
        verificationCode = input(f"Enter the verification code received on {phoneNumber} ==> ")
        sleep(5)
        self.browser.find_element_by_xpath(self.verificationCodeXpath).send_keys(verificationCode)
        self.browser.find_element_by_xpath(self.verifyXpath).click()

        # Page ==> 4
        sleep(10)
        self.browser.find_element_by_xpath(self.dayXpath).send_keys(day)
        self.browser.find_element_by_xpath(self.yearXpath).send_keys(year)

        monthOptions = Select(self.browser.find_element_by_xpath(self.monthDropDownXpath))
        monthOptions.select_by_visible_text(month.capitalize())

        genderOptions = Select(self.browser.find_element_by_xpath(self.genderDropDownXpath))
        genderOptions.select_by_visible_text(gender.capitalize())

        self.browser.find_element_by_xpath(self.thirdPageNext).click()

        # Page 5
        sleep(5)
        self.browser.find_element_by_xpath(self.skipXpath).click()

        # Page 6
        sleep(5)
        self.browser.find_element_by_xpath(self.agreeXpath).click()

        print("Account Created Successfully !!")

    def username(self, username):
        self.browser.find_element_by_xpath(self.userNameXpath).send_keys(username)
        self.browser.find_element_by_xpath("//html").click()
        sleep(1)
        try:
            err = self.browser.find_element_by_css_selector('.o6cuMc')
            print(err.text)
            print('Using the first available user name')
            sleep(1)
            self.browser.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[2]/div/ul/li[2]/button').click()
        except NoSuchElementException:
            print(1)


if __name__ == '__main__':
    details = {
        'firstName': 'First',
        'lastName': 'Last',
        'username': 'dfhdgfhfgfghfghgfh',
        'password': '',
        'phoneNumber': '',
        'month': 'January',
        'day': '1',
        'year': '1998',
        'gender': 'male'

    }
    s = SignUP()
    s.account(inputParams=details)
