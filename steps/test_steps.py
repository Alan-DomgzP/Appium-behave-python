from behave import *
from screens.test_screen import TestScreen


@Step("we are on the automation practice page")
def step_impl(context):
    test = TestScreen(context)
    test.goTo()


@Step("we type {entry} on the suggession input")
def step_impl(context, entry):
    test = TestScreen(context)
    test.fill_field(entry, test.suggestionInput)


@Then("we validate {country} is in the list")
def step_impl(context, country):
    test = TestScreen(context)
    test.getCountriesList(country)


@Step("select the country {country}")
def step_impl(context, country):
    test = TestScreen(context)
    test.select_item_in_list(test.sugesstionResults, country)


@Then("we validate that {country} is shown in the input")
def step_impl(context, country):
    test = TestScreen(context)
    test.validateInputValue(country)


@When("we click on the dropdown example")
def step_impl(context):
    test = TestScreen(context)
    test.tapDropdown()


@Then("we select {menu_option} option")
def step_impl(context, menu_option):
    test = TestScreen(context)
    test.select_dropdown_value(menu_option)


@Step("we validate that {menu_option} is the value shown in the dropdown")
def step_impl(context, menu_option):
    test = TestScreen(context)
    test.validateDropdownText(menu_option)


@When("we fill the alert input with {message}")
def step_impl(context, message):
    test = TestScreen(context)
    mensaje = message.replace("\"", "")
    test.fill_field(mensaje, test.alertInput)


@Then("we click the {option} button")
def step_impl(context, option):
    test = TestScreen(context)
    test.clickAlertButton(option)
