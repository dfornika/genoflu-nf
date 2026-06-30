#!/bin/env python

import argparse
import csv
import json

def get_threshold_from_genotype_list_used_header(list_used_header: str) -> float|None:
    """Parse the percent similarity threshold out of the header"""
    pct_str = list_used_header.split(',')[1].strip('_')
    threshold_str = pct_str.split('=')[1].rstrip('%')
    try:
        threshold = float(threshold_str)
    except ValueError:
        threshold = None

    return threshold

def parse_genotype_list_used(list: str) -> list:
    """
    Parse the genotype list used string into a dictionary
    """
    parsed = []
    for item in list.split(','):
        parsed.append(item.strip())
    return parsed

def parse_genotype_mismatch_list(list: str) -> list:
    """
    Parse the genotype mismatch list string into a list of dictionaries
    """
    parsed = []
    for item in list.split(','):
        val = None
        try:
            val = int(item)
        except ValueError as e:
            try:
                val = float(item)
            except ValueError as e:
                print(f"Error parsing {item} as float: {e}")
                val = None
        parsed.append(val) 
    return parsed

def parse_genotype_percent_match_list(list_str)-> list:
    """
    Parse the genotype percent match list string into a list of floats
    """
    parsed = []
    for item in list_str.split(','):
        item = item.strip().rstrip("%")
        val = None
        try:
            val = float(item)
        except ValueError as e:
            print(f"Error parsing {item} as float: {e}")
            val = None
        parsed.append(val) 
    return parsed

def parse_date(date_str) -> tuple:
    """
    Parse a date string in the format YYYY-MM-DD_HH-MM-SS into a tuple of (date, timestamp)
    """
    date_and_timestamp = (None, None)
    try:
        date, time_str = date_str.split('_')
        (hours, minutes, seconds) = time_str.split('-')
        timestamp = f"{date}T{hours}:{minutes}:{seconds}"
        date_and_timestamp = (date, timestamp)
    except ValueError as e:
        print(f"Error parsing {date_str} as date and timestamp: {e}")

    return date_and_timestamp

def main(args):
    with open(args.input, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            parsed_row = {
                'pct_similarity_threshold': None
            }
            for original_k, v in row.items():
                k = original_k.strip().lower().replace(' ', '_')
                if k.startswith('genotype_list_used'):
                    threshold = get_threshold_from_genotype_list_used_header(k)
                    parsed_row['pct_similarity_threshold'] = threshold
                    genotype_list_used = parse_genotype_list_used(v)
                    parsed_row['genotype_list_used'] = genotype_list_used
                elif k == 'genotype_percent_match_list':
                    genotype_percent_match_list = parse_genotype_percent_match_list(v)
                    parsed_row['genotype_percent_match_list'] = genotype_percent_match_list
                elif k == 'genotype_mismatch_list':
                    genotype_mismatch_list = parse_genotype_mismatch_list(v)
                    parsed_row['genotype_mismatch_list'] = genotype_mismatch_list
                elif k == 'date':
                    date, timestamp = parse_date(v)
                    parsed_row['date'] = date
                    parsed_row['timestamp'] = timestamp
                else:
                    parsed_row[k] = v
                
            print(json.dumps(parsed_row, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    main(args)