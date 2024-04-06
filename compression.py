"""Minify and un-minify json files."""

from io import TextIOWrapper
import json
import os

ORIGINAL_PATH = os.path.join('data', 'sorted_schedules.json')
MINIFY_PATH = os.path.join('data', 'minified_sorted_schedules.json')

def minify(read_file: TextIOWrapper, write_file: TextIOWrapper):
    json.dump(json.load(read_file), write_file)

def expand(read_file: TextIOWrapper, write_file: TextIOWrapper, indent: int =2):
    json.dump(json.load(read_file), write_file, indent=indent)
