def check_error(tag_error: dict, check_data: dict):
    errors = {}
    for name_error, type_error in tag_error.items():
        if not check_data.get(name_error, False) or not isinstance(check_data[name_error], type_error):
            errors[
                name_error] = f'There is no field {name_error} or incorrect input, input type not equals {type_error.__name__}'
    return errors
