import json
import sys
from collections.abc import Mapping, Iterable

def load_json_file(file_name):
    try:
        with open(file_name, 'r') as file:
            # Parse the file content as JSON
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_schema(obj, path=""):
    """ Recursively finds the schema of the given JSON object. """
    schema = {}

    if isinstance(obj, Mapping):
        for k, v in obj.items():
            new_path = f"{path}/{k}" if path else k
            schema[new_path] = get_schema(v, new_path)
    elif isinstance(obj, Iterable) and not isinstance(obj, str):
        item_schemas = [get_schema(item, path) for item in obj]
        schema[path] = item_schemas[0] if item_schemas else "Empty List"
    else:
        schema[path] = type(obj).__name__

    return schema

def print_schema(json_obj):
    """ Prints the schema of the JSON object. """
    schema = get_schema(json_obj)
    #print(json.dumps(schema, indent=4))

    #for path, data_type in schema.items():
    #    print(f"{path}: {data_type}")


def main():
    file_name = sys.argv[1]  # Replace with your file name
    json_data = load_json_file(file_name)

    if json_data is not None:
        while True:
            print("JSON Data Loaded Successfully:")
            k = int(input())
            stri = json.dumps(json_data[k], indent=4)
            print(stri)
            print ("Schema:")
            print_schema(json_data[k])
            print(json_data[k]['comments'][0]['title'])
if __name__ == "__main__":
    main()
