"""
Minify and un-minify json files
"""

from io import TextIOWrapper
import json

def minify(readFile: TextIOWrapper, writeFile: TextIOWrapper):
    json.dump(json.load(readFile), writeFile)

def expand(readFile: TextIOWrapper, writeFile: TextIOWrapper, indent: int =2):
    json.dump(json.load(readFile), writeFile, indent=indent)

def testMinify():
    with open('sortedSchedules.json') as rf:
        with open('minifiedSortedSchedules.json', 'w') as wf:
            minify(rf, wf)

# def testExpand():
#     with open('minifiedSortedSchedules.json') as rf:
#         with open('expandedSortedSchedules.json', 'w') as wf:
#             expand(rf, wf)
