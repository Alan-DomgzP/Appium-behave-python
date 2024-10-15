# from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.by import By


class BaseActions(object):

    def __init__(self, mobile, platform, app):
        self.driver = mobile
        self.platform = platform
        self.app = app
        self.wait = WebDriverWait(self.driver, 5)
        self.BROWSERS = {'chrome'}

    # *************************************************************************************** #
    # *                           SELENIUM FUNCTIONS                                        * #
    # *************************************************************************************** #

    def navigateTo(self, url):
        self.driver.get(url)

    def click_element(self, locator):
        if isinstance(locator, WebElement):
            locator.click()
        else:
            self.get_element(locator).click()

    def select_item_in_list(self, locator, element_to_find):
        element_list = self.get_list_of_elements(locator)
        for element in element_list:
            if element.text == element_to_find:
                self.driver.implicitly_wait(1)
                self.tap_or_click_element(element)
                break

    # *************************************************************************************** #
    # *                           GENERIC FUNCTIONS                                         * #
    # *************************************************************************************** #
    def switch_context(self, driver_context):
        self.driver.switch_to.context(driver_context)

    def hide_keyboard(self):
        self.driver.hide_keyboard()

    def get_list_of_elements(self, locator):
        return self.get_elements(locator)

    def get_element_in_list(self, value, locator):
        element_list = self.get_list_of_elements(locator)
        for item in element_list:
            if item.text == value:
                return item

    def get_element_attribute(self, locator, attribute):
        element = self.get_element(locator)
        return element.get_attribute(attribute)

    def get_element(self, locator):
        return self.wait.until(ec.presence_of_element_located( locator ))

    def get_elements(self, locator):
        return self.wait.until(ec.presence_of_all_elements_located( locator ))

    def fill_field(self, value, locator):
        element = self.get_element(locator)
        element.clear()
        element.send_keys(value)

    def tap_or_click_element(self, locator):
        try:
            try:
                if self.app.lower() in self.BROWSERS:
                    self.handle_web_click(locator)
                else:
                    self.handle_mobile_tap(locator)
            except Exception as e:
                print(f"Application '{self.app}' not supported: {e}")
        except Exception as e:
            print(f"Error in tap_or_click_element: {e}")

    def handle_web_click(self, locator):
        try:
            self.click_element(locator)
        except Exception as e:
            print(f"Element could not be clicked in web: {e}")

    def handle_mobile_tap(self, locator):
        try:
            self.tap_element(locator)
            print('Element tapped')
        except Exception as e:
            print(f"Element could not be tapped on mobile: {e}")


    # *************************************************************************************** #
    # *                           APPIUM FUNCTIONS                                         * #
    # *************************************************************************************** #

    def tap_element(self, locator):
        try:
            element = self.get_element_location(locator)
            size = self.get_element_size(locator)
            x, y = self.get_element_center(element['x'], element['y'], size)
            self.driver.tap([(x, y)])
        except Exception as e:
            print(f"Could not tap element: {e}")

    def get_element_location(self, element_or_locator):
        return self.get_element(element_or_locator).location

    def get_element_center(self, coordinate_x, coordinate_y, size):
        x = coordinate_x + (size['width'] / 2)
        y = coordinate_y + (size['height'] / 2)
        return self.adjust_coordinates_to_screen(x, y)

    def get_element_size(self, locator):
        return self.get_element(locator).size

    def get_screen_size(self):
        return self.driver.get_window_size()

    def adjust_coordinates_to_screen(self, x, y):
        window_size = self.get_screen_size()

        screen_width = window_size['width']
        screen_height = window_size['height']

        if x < 0:
            x = 1
        elif x > screen_width:
            x = screen_width - 1

        if y < 0:
            y = 1
        elif y > screen_height:
            y = screen_height - 1

        return x, y

    # SWIPE FUNCTIONS ------------------------------------------------------------------
    # DEFAULT SWIPES FROM THE CENTER OF THE SCREEN (UP, DOWN, RIGHT, LEFT)
    def default_swipe(self, direction):
        swipe_params = {
            'up': (0.5, 0.8, 0.5, 0.35),
            'down': (0.5, 0.35, 0.5, 0.8),
            'left': (0.85, 0.5, 0.15, 0.5),
            'right': (0.15, 0.5, 0.85, 0.5)
        }

        start_x_percentage, start_y_percentage, end_x_percentage, end_y_percentage = swipe_params[
            direction]

        size = self.get_screen_size()
        start_x = size['width'] * start_x_percentage
        start_y = size['height'] * start_y_percentage
        end_x = size['width'] * end_x_percentage
        end_y = size['height'] * end_y_percentage
        self.driver.swipe(start_x, start_y, end_x, end_y, duration=500)

    def swipe_multiple_times(self, direction, times=5):
        for i in range(0, times):
            self.default_swipe(direction)

    def swipe_and_find_element(self, locator, direction='up'):
        for _ in range(5):
            if self.get_element(locator).is_displayed():
                return True
            self.driver.implicitly_wait(int(1))
            self.default_swipe(direction)
        return False