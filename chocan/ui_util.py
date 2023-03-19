import output_system
import input_system

def ask_for_string(prompt: str, length: int, optional: bool = False) -> str:
    while True:
        try:
            output_system.display("\n" + prompt)
            result = input_system.get_input(length)
            if not optional and (result == None or result == ""):
                raise ValueError
        except ValueError:
            output_system.display("Invalid data. Try again.")
            continue
        break
    return result

def ask_for_int(prompt: str, min: int, max: int) -> int:
    while True:
        try:
            output_system.display("\n" + prompt)
            # I chose 10 here because the largest integer we will ever read in is 9
            # and I want to make sure that input that is too long is not truncated and accepted
            result = int(input_system.get_input(10))
            if result < min or result > max:
                raise ValueError
        except ValueError:
            output_system.display("Invalid data. Try again.")
            continue
        break
    return result

def ask_for_float(prompt: str, min: int, max: int) -> float:
    while True:
        try:
            output_system.display("\n" + prompt)
            result = float(input_system.get_input(10))
            if result < min or result > max:
                raise ValueError
        except ValueError:
            output_system.display("Invalid data. Try again.")
            continue
        break
    return result

def ask_yes_or_no(prompt: str) -> bool:
    while True:
        try:
            output_system.display("\n" + prompt)
            # I chose 2 here to make sure that input that is longer than 1 char
            # is not truncated and accepted
            result = input_system.get_input(2)
            result = result.lower()
            if result != "y" and result != "n":
                raise ValueError
            if result == "n":
                return False
        except ValueError:
            output_system.display("Invalid data. Try again.")
            continue
        break
    return True

def fee_format(n : float) -> str:
    return f'${(n / 100):0.2f}'
