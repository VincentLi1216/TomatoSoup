import json
from util_warning import *

def put_json_data(file_name, dict):

    try:
        # Serializing json
        json_object = json.dumps(dict, indent=4)

        # Writing to sample.json
        with open(file_name, "w") as outfile:
            outfile.write(json_object)
    except:
        warning("Can NOT put to the json file!")


def get_json_data(file_name, key):
    try:
        with open(file_name) as f:
            data = json.load(f)
            return data[key]
    except:
        warning("Can NOT read from the json file!")


if __name__ == "__main__":
    print(get_json_data("user_pref.json", "last_used_camera"))
    # put_json_data("user_pref.json", {"last_used_camera":2})