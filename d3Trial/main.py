#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import sys
import gzip
import pandas as pd
from datetime import datetime


def fatal(msg):
    print(msg)
    sys.exit(1)


def read_index_file(path):
    data = Path(path).read_text()
    return list(map(json.loads, data.splitlines()))


def build_query_patterns(query):
    patterns = {}

    for s in args.query:
        m = re.match("([A-Za-z0-9]+)=(\S+)$", s)
        if m is None:
            raise ValueError(f"Invalid query {s!r}.")
        key, value = m.groups()
        pattern = re.compile(value)
        patterns[key] = pattern

    return patterns

parser = argparse.ArgumentParser()
parser.add_argument("--root", default=".", type=Path, help="root directory to work in")
parser.add_argument("query", nargs="*", help="query terms")
args = parser.parse_args()

patterns = build_query_patterns(args.query)

try:
    index = read_index_file(Path(args.root, "index.ndjson"))
except FileNotFoundError:
    fatal("no index.json file in data folder")
except json.JSONDecodeError:
    fatal("invalid index.ndjson file")


def item_matches_patterns(item, patterns):
    return all(k in item["key"] and pattern.search(item["key"][k]) for k, pattern in patterns.items())

selected_items = [item for item in index if item_matches_patterns(item, patterns)]

      
with Path(args.root, "data.ndjson.gz").open("rb") as f:
    data_string = ""
    for item in selected_items:
        f.seek(item["offset"])
        data = f.read(item["size"])
        sys.stdout.write(gzip.decompress(data).decode())
        data_string = data_string + gzip.decompress(data).decode()
        


#{'key': {'date': '2021-06-16', 'name': 'iio.in_humidityrelative_input', 'node': '000048b02d15bc72', 'plugin': 'plugin-metsense:0.1.1', 'sensor': 'bme680'}, 'offset': 1548244, 'size': 29981}

def aggregate_data():
    agg_dict = {}
    for item in index:
        #TODO: consider version numbers
        plugin = item['key']['plugin']
        date = item['key']['date']
        nodeid = item['key']['node']
        # create key 'plugin' if it does not exist
        if plugin not in agg_dict:
            agg_dict[plugin] = {}
        # if date is in 'plugin', add 1 to count
        if date in agg_dict[plugin]:
            agg_dict[plugin][date] = agg_dict[plugin][date] + 1
        # else set count to 1
        else:
            agg_dict[plugin][date] = 1
    prettyprint = json.dumps(agg_dict)
   # print(type(result))
    json_object = json.loads(prettyprint)
    json_format = json.dumps(json_object, indent = 2)
    return json_format

print(aggregate_data())