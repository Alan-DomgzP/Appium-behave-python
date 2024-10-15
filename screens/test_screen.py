from time import sleep

from selenium.webdriver.common.by import By
# from appium.webdriver.common.appiumby import AppiumBy
from utils.base_actions import BaseActions


class TestScreen(BaseActions):
    def __init__(self, context):
        platform = context.PLATFORM
        app = context.APP
        super().__init__(context.driver, platform, app)
        self.suggestionInput = (By.XPATH, "//input[@id='autocomplete']")
        self.sugesstionResults = (By.XPATH, "//div[starts-with(@id, 'ui-id-')]")

        self.dropdownLabel = ( By.XPATH, '//legend[normalize-space()="Dropdown Example"]')
        self.dropdownElement = (By.XPATH, "//select[@id='dropdown-class-example']")
        # self.dropdown_options = "//option[@value='{}']"
        self.dropdown_options = "//android.widget.CheckedTextView[@resource-id='android:id/text1' and @text='{}']"
        self.alertInput = (By.XPATH, "//input[@id='name']")
        self.alertButton = (By.XPATH, "//input[@id='alertbtn']")
        self.confirmButton = (By.XPATH, "//input[@id='confirmbtn']")

    def goTo(self):
        self.navigateTo('https://rahulshettyacademy.com/AutomationPractice/')
        assert "Practice Page" in self.driver.title

    def getCountriesList(self, country):
        countries = self.get_list_of_elements(self.sugesstionResults)
        countrylist = []

        for element in countries:
            countrylist.append(element.text)

        print(countrylist)
        assert country in countrylist, f"´{country}´ is not on the list"

    def validateInputValue(self, country):
        selected_value = self.get_element_attribute(self.suggestionInput,"value")
        try:
            assert selected_value == country
        except AssertionError as error:
            print(f"Assertion Failed: {error}")

    def tapDropdown(self):
        self.tap_or_click_element(self.dropdownElement)

    def select_dropdown_value(self, option):
        self.switch_context('NATIVE_APP')
        value = (By.XPATH, self.dropdown_options.format(option))
        assert self.get_element(value)
        self.tap_element(value)
        self.switch_context('CHROMIUM')
        self.click_element(self.dropdownLabel)

    def validateDropdownText(self, menu_option):
        self.switch_context('NATIVE_APP')
        element = (By.XPATH, '//android.view.View[@resource-id="dropdown-class-example"]')
        element_txt = self.get_element(element).text
        self.switch_context('CHROMIUM')
        assert (element_txt == menu_option)

    def clickAlertButton(self, option):
        button_to_click = self.alertButton if option == 'alert' else self.confirmButton
        self.get_element(button_to_click).click()
        print(self.get_element_attribute(button_to_click, 'text'))
        assert not self.get_element(button_to_click), "El elemento fue encontrado, pero se esperaba que no lo fuera."

    def validateAlertMessage(self):
        self.switch_context('NATIVE_APP')
        alert = (By.XPATH, '//android.widget.TextView[@resource-id="com.android.chrome:id/message"]')
        element = self.get_element(alert)
        assert (f"Hello Automation Challenge, share this practice page and share your knowledge" == element.txt)
        self.switch_context('CHROMIUM')