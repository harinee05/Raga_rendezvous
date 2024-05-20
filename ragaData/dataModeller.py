import json
import glob
import os
import glob
import chardet


def raga_converter(data):
    r_name = data["ragas"]["name"]
    r_id = data["ragas"]["id"]

    r_json = {}
    r_json["name"] = r_name.lower()
    r_json["arohanas"] = {str(d["order"]): d["swara_id"] for d in data["arohanas"]}
    r_json["avarohanas"] = {str(d["order"]): d["swara_id"] for d in data["avarohanas"]}

    return r_json, r_id


def janya_converter(data):
    r_name = data["ragas"]["name"]
    r_id = data["ragas"]["id"]

    r_json = {}
    r_json["name"] = r_name.lower().replace("\u0101", "a").replace("\u016b", "u")
    r_json["parent_id"] = data["melakarta_janya_links"]["raga_id"]
    r_json["arohanas"] = {str(d["order"]): d["swara_id"] for d in data["arohanas"]}
    r_json["avarohanas"] = {str(d["order"]): d["swara_id"] for d in data["avarohanas"]}

    return r_json, r_id


def swara_converter(data):

    r_json = {}
    for i in range(len(data)):
        r_json[str(i + 1)] = data[i]

    return r_json


ragaFiles = glob.glob("ragas/*.json")
raga_dict = {}
for file in ragaFiles:
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
        data, r_id = raga_converter(data)
        raga_dict[r_id] = data

with open("janakas_without_swara.json", "w") as fp:
    json.dump(raga_dict, fp, indent=4)


janyaFiles = glob.glob("ragas/janyas/*.json")
janya_dict = {}
for file in janyaFiles:
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
        data, r_id = janya_converter(data)
        janya_dict[r_id] = data

with open("janyas_without_swara.json", "w") as fp:
    json.dump(janya_dict, fp, indent=4)


with open("swaras/swaras.json", encoding="utf-8") as f:
    data = json.load(f)
    swara_dict = swara_converter(data)

with open("swaras.json", "w") as fp:
    json.dump(swara_dict, fp, indent=4)


for k in raga_dict.keys():
    for l in raga_dict[k]["arohanas"].keys():
        raga_dict[k]["arohanas"][l] = swara_dict[str(raga_dict[k]["arohanas"][l])][
            "notation"
        ]

    for l in raga_dict[k]["avarohanas"].keys():
        raga_dict[k]["avarohanas"][l] = swara_dict[str(raga_dict[k]["avarohanas"][l])][
            "notation"
        ]

with open("janakas_with_swara.json", "w") as fp:
    json.dump(raga_dict, fp, indent=4)


for k in janya_dict.keys():
    for l in janya_dict[k]["arohanas"].keys():
        janya_dict[k]["arohanas"][l] = swara_dict[str(janya_dict[k]["arohanas"][l])][
            "notation"
        ]

    for l in janya_dict[k]["avarohanas"].keys():
        janya_dict[k]["avarohanas"][l] = swara_dict[
            str(janya_dict[k]["avarohanas"][l])
        ]["notation"]

with open("janyas_with_swara.json", "w") as fp:
    json.dump(janya_dict, fp, indent=4)


final_json = {}
final_json["janaka"] = raga_dict
final_json["janya"] = janya_dict
with open("ragas.json", "w") as fp:
    json.dump(final_json, fp, indent=4)
