import json

def _get_value_from_json(json_file, keys):
    with open(json_file, 'r') as file:
        data = json.load(file)
        current = data
        try:
            for key in keys:
                current = current[key]
            return current
        except KeyError:
            return f"Key '{key}' not found in the JSON file."

def get_json_value(json_dir_name, json_file):

    #print(f"josn file path: {json_file}")

    #json_file_path = f"{json_dir_name}/{json_file}" # Change this to the path of your JSON file
    given_key = ["source","identifier","value"]  # Change this to the key you want to retrieve the value for

    value = _get_value_from_json(json_file, given_key)
    #print(f"The value of '{given_key}' is: {value}")
    
    return value