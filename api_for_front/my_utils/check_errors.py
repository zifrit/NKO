

def check_error(tag_error: list[str], check_data: dict):
    errors = {}
    for name_error in tag_error:
        if not check_data.get(name_error, False) or \
                (not check_data[name_error] and isinstance(check_data[name_error], str)):
            errors[name_error] = f'There is no field {name_error} or incorrect input'
    return errors
