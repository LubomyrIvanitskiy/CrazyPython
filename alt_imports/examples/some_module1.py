from tags import tag


@tag("utils.string", "utils.validation")
def validate_phone_ua(phone):
    return phone.startswith("+380") and len(phone) == 13
