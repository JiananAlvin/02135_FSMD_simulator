def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


d1 = {"xjn": "son"}
d2 = {"fwj": "dad"}
d3 = merge_dicts(d2, d1)
d4 = {}
d4.update(d1)
d4.update(d2)
print(d4)