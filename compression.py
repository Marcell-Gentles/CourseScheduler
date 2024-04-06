"""
Minify and un-minify json files
"""

from io import TextIOWrapper
import json
import os

ORIGINAL_PATH = os.path.join('data', 'sorted_schedules.json')
MINIFY_PATH = os.path.join('data', 'minified_sorted_schedules.json')

def minify(readFile: TextIOWrapper, writeFile: TextIOWrapper):
    json.dump(json.load(readFile), writeFile)

def expand(readFile: TextIOWrapper, writeFile: TextIOWrapper, indent: int =2):
    json.dump(json.load(readFile), writeFile, indent=indent)

def test_minify():
    with open(ORIGINAL_PATH) as rf:
        with open(MINIFY_PATH, 'w') as wf:
            minify(rf, wf)
