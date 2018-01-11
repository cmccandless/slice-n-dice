#!/usr/bin/env python
import argparse
import json
from dice import dice

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('data_file')
parser.add_argument('--schema', default='schema.json')

opts = parser.parse_args()

with open(opts.data_file) as f:
    data = json.load(f)

with open(opts.schema, 'r') as f:
    schema = json.load(f)

print(json.dumps(dice(data, schema), indent=2))
