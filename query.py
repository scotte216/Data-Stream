import argparse
from datetime import datetime
from Common.functions import add_data, get_filtered_stb, get_data

parser = argparse.ArgumentParser(description='Data-stream import and searching. Expected input data-stream line\n' +
                                 'of the form: STB|TITLE|PROVIDER|DATE|REVENUE|TIME\n')
parser.add_argument('-i', dest='filename', help='import FILENAME to import data to datastore')
parser.add_argument('-s', dest='select',
                    help='SELECT from comma separated list of columns (STB,TITLE,PROVIDER,DATE,REV,TIME)')
parser.add_argument('-f', dest='filter',
                    help='FILTER from one column=value pair. CASE SENSITIVE. ex -f date=2017-04-21')
parser.add_argument('-o', dest='order',
                    help='ORDER from comma separated list of columns (STB,TITLE,PROVIDER,DATE,REV,TIME)')
args = parser.parse_args()
count = 0


"""
If importing data:
Import data stream from argument filename. Expected format:

STB|TITLE|PROVIDER|DATE|REVENUE|TIME\n

"""
if args.filename:
    with open(args.filename, 'r') as file:
        for line in file:
            box_id, title, provider, date, revenue, time = line.rstrip('\r\n').split('|')
            count += 1
            try:
                time = datetime.strptime(time, '%H:%M')
                date = datetime.strptime(date, '%Y-%m-%d')
                data = {
                    'stb': box_id,
                    'date': date.strftime('%Y-%m-%d'),
                    'title': title,
                    'provider': provider,
                    'rev': "{0:.2f}".format(float(revenue)),
                    'time': time.strftime('%H:%M')
                }
                add_data(data)
            except ValueError as e:
                print("Mal-formatted line. Skipping.")
# Else, retrieving data. Data retrieval from SELECT, FILTER, and ORDER arguments
else:
    # Error checking retrieval arguments
    columns = {'stb', 'title', 'provider', 'date', 'rev', 'time'}
    selection = args.select.lower().split(',') if args.select else None
    if not selection or not set(selection) < columns:
        print("Invalid SELECT argument(s). See --help for help.")
        exit(1)

    order = args.order.lower().split(',') if args.order else None
    if order and not set(order) < columns and not set(order) < set(selection):
        print("Invalid ORDER arguments(s). See --help for help.")
        exit(1)

    filter_by = ()
    if args.filter:
        key, value = tuple(args.filter.split('='))
        if key not in columns:
            print("Invalid FILTER argument(s). See --help for help.")
            exit(1)
        if key == 'rev':
            try:
                value = "{0:.2f}".format(float(value))
            except ValueError:
                print("Invalid number for rev filter.")
                exit(1)

        filter_by = (key, value)

    # Retrieve set of matching STB id numbers based on the filter
    matching_stb = get_filtered_stb(filter_by)

    # If there are any matching STB id numbers, get actual data, order, and print SELECT results.
    if matching_stb:
        results = get_data(matching_stb, selection, filter_by, order)
        # Print results in order of SELECT
        for entry in results:
            print(','.join([entry[key] for key in selection]))
