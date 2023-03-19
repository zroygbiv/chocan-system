from datetime import datetime
from chocan import (
    input_system,
    output_system,
    member_system,
    service_system,
    constants,
    ui_util,
    provider_directory_system
)


def get_service_record_input() -> dict:
    provider_number = ui_util.ask_for_int("Provider Number: ", constants.MIN_USER_NUM, constants.MAX_USER_NUM)
    member_number   = ui_util.ask_for_int("Member Number: ", constants.MIN_USER_NUM, constants.MAX_USER_NUM)
    member_name     = ui_util.ask_for_string("Member Name: ", constants.MAX_NAME)
    service_code    = ui_util.ask_for_int("Service Code: ", constants.MIN_CODE, constants.MAX_CODE)
    # turn dollar float into cents int (ex. 999.99 = 99999)
    fee             = int(ui_util.ask_for_float("Service Fee ($): ", constants.MIN_FEE, constants.MAX_FEE) * 100)
    comments        = ui_util.ask_for_string("Comments: ", constants.MAX_COMMENT, True)
    date_of_service = datetime.now().isoformat()
    date_received   = datetime.now().isoformat()

    record  = {
        'provider_number': provider_number,
        'member_number': member_number,
        'member_name': member_name,
        'service_code': service_code,
        'fee': fee,
        'date_of_service' : date_of_service,
        'date_received' : date_received,
        'comments' : comments
    }
    return record

# Provider Menu
###############################################################################
def display_provider_ui_menu() -> None:
    output_system.display(
        "\n\n"
        "************* PROVIDER MENU ************\n"
        "1. Check In Member\n"
        "2. Bill Member\n"
        "3. Provider Directory\n"
        "4. Exit\n"
        "----------------------------------------"
    )

def run_provider_ui() -> None:
    while True:
        display_provider_ui_menu()
        selection = input_system.get_input(1)
        match selection:
            case '1': run_checkin_member_ui()
            case '2': run_bill_member_ui()
            case '3':
                provider_directory_system.generate_provider_directory()
                output_system.display("Provider Directory generated.")
            case '4': break
            case _:
                output_system.display(f'Unknown selection {selection}')

def run_checkin_member_ui() -> None:
    number = ui_util.ask_for_int("Enter Member Number: ", constants.MIN_USER_NUM, constants.MAX_USER_NUM)
    member = member_system.get_active_member(number)
    if member == None:
        output_system.display("That Member does not exist.")
    elif member.active == False:
        output_system.display("Member Suspended")
    else:
        output_system.display("Validated")

def run_bill_member_ui() -> None:
    number = ui_util.ask_for_int("Enter Member Number: ", constants.MIN_USER_NUM, constants.MAX_USER_NUM)
    member = member_system.get_active_member(number)
    if member == None:
        output_system.display("That Member does not exist.")
    elif member.active == False:
        output_system.display("Member Suspended")
    else:
        output_system.display("Validated")
        run_create_service_record_ui()

def run_create_service_record_ui() -> None:
    record = get_service_record_input()
    try:
        service_record = service_system.create_service_record(
            record['provider_number'],
            record['member_number'],
            record['member_name'],
            record['service_code'],
            record['fee'],
            record['date_of_service'],
            record['date_received'],
            record['comments']
        )
        output_system.display("\nService Record Created!\n")
        output_system.display(
            f'Provider Number: #{service_record.provider_number}\n'
            f'Member Number: {service_record.member_number}\n'
            f'Member Name: {service_record.member_name}\n'
            f'Service Code: {service_record.service_code}\n'
            f'Fee: {ui_util.fee_format(service_record.fee)}\n'
            f'Date of Service: {service_record.date_of_service_pretty()}\n'
            f'Date Received: {service_record.date_received_pretty()}\n'
            f'Comments: {service_record.comments}\n'
        )
    except service_system.MaxFeeError:
        output_system.display("\nWeekly service fee has exceeded the $99,999.99 limit.")