import json
import csv
import sys
from pathlib import Path


"""
Replace FILTER_TXT with the path/name of the .txt file that will hold the filter name/filter term(s) (see format below);
The results of the filter will then be written to FILTER_TXT as well
Replace DATABASE with the path/name of the .json that contains the database's contents (i.e., the items to be filtered)

The format of the text file that is input should be:
Line 1: Category to be filtered (or the name of the column within the SQL table)
Line 2: Term to be filtered within category 
Line 3: Category...
Line 4: Term...
etc...
"""
FILTER_TXT = 'filter_terms.txt'
OUTPUT_JSON = 'json_output.json'
DATABASE = 'case_summaries.json'
DATE_MAP = 'date_list.csv'


def create_filter_list():
    try:
        filter_file = open(FILTER_TXT, 'r')
        item_list = filter_file.read().splitlines()
        filter_file.close()
        filter_json(item_list)
    except FileNotFoundError:
        sys.exit("Input file not found.")


def filter_json(item_list):
    check_if_legal(item_list)
    run_filter(item_list, DATABASE)


def check_if_legal(item_list):
    """
    Determines if the txt that contains the filter terms is legal. If not, the entire unfiltered database is written to
    FILTER_TXT and an error is raised. The error can be removed from function if you do not wish this error to result
    in a program fault.
    """
    if len(item_list) < 2:
        endnow = json.loads(Path(DATABASE).read_text())
        unfiltered = open(FILTER_TXT, 'w+')
        now = json.dumps(endnow, indent=3)
        unfiltered.write(now)
        unfiltered.close()
        sys.exit("The filter parameters are incomplete or illegal. Try your filter again")


def run_filter(item_list, txt_input):
    jout = make_json(item_list, txt_input)
    filtered = open(OUTPUT_JSON, 'w+')
    filtered.write(jout)
    filtered.close()
    check_mult(item_list)


def make_json(item_list, txt_input):
    """
    This function loads the json and makes it text. The terms iterate and check if the any part of the
    substring(filter term) is contained in the string(json text). If so, it is written to the output json).
    :return: the post-filter json
    """
    kind = item_list[0].lower()
    term = item_list[1]
    jdict = json.loads(Path(txt_input).read_text().lower())
    out_dict = [x for x in jdict if term in x[kind]]
    jout = json.dumps(out_dict, indent=3)
    return jout


def check_mult(item_list):
    """
    checks if there is more than 1 filter pair being run; if so, remove last filter and recurse new item_list and
    new FILTER_TXT JSON back to the run_filter function. If there is not an even number of items remaining in the list,
    the list is not legal and the process stops.
    """
    if len(item_list) >= 4 and len(item_list) % 2 == 0:
        item_list.pop(0)
        item_list.pop(0)
        run_filter(item_list, FILTER_TXT)
    else:
        return


def date_list():
    term_list = []
    json_dict = json.loads(Path(OUTPUT_JSON).read_text())
    for i in range(len(json_dict)):
        for key in json_dict[i]:
            if key == 'term':
                term_list.append(json_dict[i][key])
    create_csv(term_list)


def create_csv(term_list):
    with open(DATE_MAP, 'w') as f:
        write = csv.writer(f)
        write.writerow(term_list)


create_filter_list()
date_list()


