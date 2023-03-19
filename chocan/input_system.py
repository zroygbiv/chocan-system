def get_input(max : int) -> str:
    if max < 0:
        raise ValueError('max must be a non-negative integer')
    user_input = input()
    nice_input = user_input.strip()
    return nice_input[0:max]
