Feature: Automation practice
    A site to practice automation.

    Background:
    # Test 1
        Given we are on the automation practice page
    # paver run_feature test chrome android 12 emulator-5554 test

    # Test 2
    @suggestion_input
    Scenario Outline: Suggestion input example
        When we type <entry> on the suggession input
        Then we validate <country> is in the list
        And select the country <country>
        Then we validate that <country> is shown in the input

        Examples:
            | entry | country              |
            | Me    | Mexico               |
            | Uni   | United States (USA)  |
            | Uni   | United Arab Emirates |
            | Co    | Colombia             |
            | Col   | Colombia             |

    # Test 3
    @dropdown
    Scenario Outline: Get dropdown menu options
        When we click on the dropdown example
        Then we select <menu_option> option
        And we validate that <menu_option> is the value shown in the dropdown

        Examples:
            | menu_option |
            | Option2     |
            | Option3     |

    # Test 6
    @alert @test
    Scenario: Switch To Alert Example
        When we fill the alert input with "Automation Challenge"
        Then we click the alert button
#        And validate the alert text and close alert
#        When we fill the alert input with "Challenge"
#        Then we click the confirm button
#        And validate the confirm text and close alert
