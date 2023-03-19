import string
from chocan import (
    constants,
    input_system,
    output_system,
    manager_ui_system,
    provider_ui_system,
    provider_system,
    ui_util
)

def display_main_ui_menu() -> None:
    output_system.display(
        "\n\n"
        "*************** MAIN MENU **************\n"
        "1. Manager Login\n"
        "2. Provider Login\n"
        "3. Shutdown system\n"
        "----------------------------------------"
    )

def run_ui() -> None:
    while True:
        display_main_ui_menu()
        selection = input_system.get_input(1)
        match selection:
            case '1': manager_ui_system.run_manager_ui()
            case '2': verify_provider_credentials()
            case '3': quit()
            case _:
                output_system.display(f"Unknown selection {selection}")

def verify_provider_credentials() -> None:
    number = ui_util.ask_for_int("Enter Provider Number: ", constants.MIN_USER_NUM, constants.MAX_USER_NUM)
    if provider_system.verify_provider(number):
        provider_ui_system.run_provider_ui()
    else:
        output_system.display("Invalid Credentials!")