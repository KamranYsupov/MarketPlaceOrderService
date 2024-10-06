def normalize_field_name(name: str) -> str:
    """ isVerified --> is_verified """

    normalized_name = ''
    for char in name:
        if char.isupper():
            normalized_name += f'_{char.lower()}'
        else:
            normalized_name += char

    return normalized_name