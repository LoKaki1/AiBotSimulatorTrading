import json
from typing import Any, Union


def open_json(json_path: str):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)


def write_in_json(path: str, data: [dict, list]):
    json_object = open_json(path)
    json_object.update(data)
    write_json(path, json_object)


def update_json_where(path: str, relevant_key: str, value: Any, data: Union[dict, list, bytes]):
    file_data = open_json(path)
    result_data = list(
        map(
            lambda x: data if x[relevant_key] == value else x, file_data
        )
    )
    write_json(path, result_data)


def write_json(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file,
                  indent=4,
                  separators=(',', ': ')
                  )
