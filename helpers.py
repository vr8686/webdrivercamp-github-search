def gherkin_to_json(gherkin_data_type):
    mapping = {"Repos": "public_repos",
               "Gists": "public_gists",
               "Twitter": "twitter_username",
               "link": "html_url"}
    return mapping.get(gherkin_data_type, gherkin_data_type.lower())


def create_jsonpath(data):
    return '[' + ', '.join(f'"{data_type}"' for data_type in data) + ']'


def clean_bio_string(input_string=None):
    if input_string:
        # Define a list of whitespace characters to remove
        whitespace_chars = ['\r', '\n', '\t', '\f']

        # Replace each whitespace character with an empty string
        cleaned_string = input_string
        for char in whitespace_chars:
            cleaned_string = cleaned_string.replace(char, '')

        return cleaned_string
    return input_string


def add_whitespace(profile_name, position):
    if position == "before":
        return profile_name + " "
    elif position == "after":
        return " " + profile_name
