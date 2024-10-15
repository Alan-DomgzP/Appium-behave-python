from selenium.webdriver.common.by import By
from utils.base_actions import BaseActions
from utils.constants.base_constants import BaseConstants
from utils.dictionaries.sapp_negocio.tiempo_aire.planes_texts import TELEPHONE_RECHARGES, COMPANIES


class CompraTiempoAireScreen(BaseActions):
    def __init__(self, context):
        platform = context.PLATFORM
        self.app = context.APP
        self.base_constants = BaseConstants(self.app)
        super().__init__(context.driver, platform)

        if platform == "android":
            # Header
            self.btn_back = (
                By.XPATH, "//*/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView")
            self.lbl_title = (By.XPATH, "//*[contains(@text,'Tiempo aire')]")
            self.btn_close = (By.XPATH,
                              "//*/android.view.View/android.view.View/android.view.View[2]/android.view.View/"
                              "android.view.View")

            # Screen "2. ¿De qué compañía?"
            self.input_phone_number = (
                By.ID, self.base_constants.android_predicate() + "id/et_number_phone")
            self.btn_to_continue = (
                By.ID, self.base_constants.android_predicate() + "id/button")

            # Screen "2. ¿De qué compañía?"
            self.lbl_titlecard = (
                By.ID, self.base_constants.android_predicate() + "id/txtTitleCard")
            self.lbl_contentcard = (
                By.ID, self.base_constants.android_predicate() + "id/txtContentCard")
            self.lbl_title_choose_company = (
                By.ID, self.base_constants.android_predicate() + "id/tv_title_choose_company")

            # Screen "2. ¿De qué compañía?" error
            self.lbl_infoText_error = (
                By.ID, self.base_constants.android_predicate() + "id/infoText")
            self.btn_close_error = (
                By.XPATH, "//android.widget.ImageView[@content-desc='Close Icon']")

            # Screen "3. ¿Cuánto quieres recargar?"
            self.lbl_subtitle_from_company = (
                By.ID, self.base_constants.android_predicate() + "id/tv_subtitle_from_company")
            self.lbl_populares = (By.XPATH, "//*[contains(@text,'Populares')]")
            self.lbl_all_recharges = (
                By.XPATH, "//*[contains(@text,'Todas las recargas')]")

            # Screen "3. ¿Cuánto quieres recargar?" error
            self.lbl_infoText_error_2 = (
                By.ID, self.base_constants.android_predicate() + "id/tv_message")
            self.lbl_snackbar_text = (
                By.ID, self.base_constants.android_predicate() + "id/snackbar_text")
            self.btn_close_error_2 = (
                By.XPATH, "(//android.widget.ImageView[@content-desc='TODO'])[2]")

            # Screen "Sumarry"
            self.lbl_number = (
                By.XPATH, "//*/android.view.View[3]/android.widget.TextView[4]")
            self.link_edit_number = (
                By.XPATH, "(//android.widget.TextView[@text='Editar'])[1]")
            self.link_edit_company = (
                By.XPATH, "(//android.widget.TextView[@text='Editar'])[2]")
            self.link_edit_pay = (
                By.XPATH, "(//android.widget.TextView[@text='Editar'])[3]")
            self.lbl_company = (
                By.XPATH, "//*/android.view.View[3]/android.widget.TextView[7]")
            self.lbl_pay = (
                By.XPATH, "//*/android.view.View[3]/android.widget.TextView[13]")
            self.sv_bar = (
                By.XPATH, "//*[contains(@text,'Desliza para pagar')]")

            # summart_buy
            self.lbl_ticket = (
                By.XPATH, "//*/android.widget.ScrollView/android.view.View[1]/android.widget.TextView[1]")
            self.lbl_shear = (
                By.XPATH, "//*[contains(@text,'Compartir con mi cliente')]")
            self.lbl_id = (
                By.XPATH, "//*[contains(@text,'Folio de operación:')]")
            self.sv_bar = (By.XPATH, "//*[contains(@text,'Desliza para')]")

            # Exit
            self.btn_exit_sure = (By.XPATH, "//*[contains(@text,'SALIR')]")
            self.btn_cancel_sure = (
                By.XPATH, "//*[contains(@text,'CANCELAR')]")
            self.lbl_pop_exit = (
                By.XPATH, "//*[contains(@text,'No se guardarán los datos ingresados.')]")

    def select_a_carrier(self, carrier):
        iteration = 1
        for key, value in COMPANIES.items():
            if value == carrier:
                recharge_amount = (
                    By.XPATH, f"(//android.widget.ImageView[@content-desc='Selecciona'])[{iteration}]")
                self.tap_element(recharge_amount)
                break
            iteration += 1

    def select_an_amount(self, package):
        recharge_amount = (By.XPATH, "//*[contains(@text,'" + package + "')]")
        self.find_and_tap_element(recharge_amount)

    def slide_to_send_baz(self, *locator):
        size = self.driver.get_window_size()
        size_baz = self.driver.find_element(*locator).location
        start_y = size_baz['y']
        end_y = size_baz['y']
        start_x = size['width'] * 0.10
        end_x = size['width'] * 0.99
        self.driver.swipe(start_x, start_y, end_x, end_y, 500)

    def baz_slide_action(self):
        self.slide_to_send_baz(*self.sv_bar)
        try:
            self.slide_to_send_baz(*self.sv_bar)
        except:
            pass

    def validate_look_and_feel_sumary(self):
        self.assert_if_element_is_displayed(*self.lbl_number)
        self.assert_if_element_is_displayed(*self.lbl_company)
        self.assert_if_element_is_displayed(*self.lbl_pay)

    def validate_look_and_feel_tiket(self):
        self.wait_until_element_is_present(locator=self.lbl_ticket, seconds=30)
        self.assert_text_element(*self.lbl_ticket, value="Compra realizada")
        self.assert_if_element_is_displayed(*self.lbl_shear)
        self.assert_if_element_is_displayed(*self.lbl_id)

    def validate_package(self, company):
        recharge_plans = TELEPHONE_RECHARGES.get(company)
        recharge_amount = (By.XPATH, "//*[contains(@text,'" + company + "')]")
        self.assert_if_element_is_displayed(*recharge_amount)
        self.wait_until_element_is_present(
            locator=self.lbl_subtitle_from_company, seconds=30)
        for key, value in recharge_plans.items():
            package_label = (By.XPATH, "//*[contains(@text,'" + value + "')]")
            self.swipe_and_find_element(*package_label)
            self.assert_if_element_is_displayed(*package_label)

    def validate_companies(self):
        for key, value in COMPANIES.items():
            company_button = (By.XPATH, "//*[contains(@text,'" + value + "')]")
            self.assert_if_element_is_displayed(*company_button)

    def validate_recharge_invalid(self):
        self.assert_if_element_is_displayed(*self.lbl_infoText_error)
        self.tap_element(self.btn_close_error)

    def validate_insufficient_balance(self):
        self.assert_if_element_is_displayed(*self.lbl_infoText_error_2)
        self.assert_if_element_is_displayed(*self.lbl_snackbar_text)
        self.tap_element(self.btn_close_error_2)

    def edition_summary(self, data):
        self.assert_if_element_is_displayed(*self.lbl_number)
        self.assert_if_element_is_displayed(*self.lbl_company)
        self.assert_if_element_is_displayed(*self.lbl_pay)
        match data:
            case "A qué número recargas":
                self.tap_element(self.link_edit_number)
            case "De qué compañía":
                self.tap_element(self.link_edit_company)
            case "Cuánto quieres pagar":
                self.tap_element(self.link_edit_pay)

    def validateback(self):
        self.tap_element(self.btn_back)
        self.assert_if_element_is_displayed(*self.lbl_subtitle_from_company)
        self.tap_element(self.btn_back)
        self.assert_if_element_is_displayed(*self.lbl_titlecard)
        self.tap_element(self.btn_back)
        self.assert_if_element_is_displayed(*self.input_phone_number)
        self.tap_element(self.btn_close)
        self.assert_if_element_is_displayed(*self.lbl_pop_exit)
        self.tap_element(self.btn_cancel_sure)
        self.tap_element(self.btn_close)
        self.assert_if_element_is_displayed(*self.lbl_pop_exit)
        self.tap_element(self.btn_exit_sure)
