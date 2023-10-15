# --*--*--*--*--*--*- Create by bh at 2023/10/3 10:47 -*--*--*--*--*--*--
import json


def contains(s, eles):
    for ele in eles:
        if ele in s:
            return True
    return False


def choices_to_dict(choices: tuple, key_is_filed=True):
    ret = dict()
    key_index = int(not key_is_filed)
    value_index = int(key_is_filed)
    for choice in choices:
        ret[choice[key_index]] = choice[value_index]
    return ret


def display_choices(choices: tuple) -> list:
    return [{'label': choice[1], 'value': choice[0]} for choice in choices]


def json_str(origin: str):
    format_str = origin.replace('"', "'").replace("'", '"')
    return json.loads(format_str)
