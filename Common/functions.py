import json
import os

DIR = os.path.normpath(os.getcwd() + '/data/')


def create_indices(new_data):
    """
    Updates index files for faster FILTER functionality.
    :param new_data: New data to enter into data indexes. Of the form
            {
                "stb": box_id_string,
                "date": date_string YYYY-MM-DD,
                "title": title_string,
                "provider": provider_string,
                "rev": revenue_string,
                "time": time_string HH:MM
            }
            Data has been checked prior to calling function. Ideally there would be checks here in this function
            was used elsewhere.
    :return:
    """
    try:
        os.makedirs(DIR)
    except FileExistsError:
        pass

    for each in ['date', 'title', 'provider', 'rev', 'time']:
        key = new_data[each]
        filename = os.path.normpath(DIR + '/' + each + '_index.json')
        try:
            with open(filename, 'r') as data_file:
                data = json.load(data_file)
        except IOError:
            data = {}
        if key not in data:
            data[key] = []
        if new_data['stb'] not in data[key]:
            data[key].append(new_data['stb'])

        with open(filename, 'w') as data_file:
            json.dump(data, data_file)
    return


def add_data(new_data):
    """
    add_data from the data stream into the data store.
    :param new_data: New data to enter into datastore. Of the form
            {
                "stb": box_id_string,
                "date": date_string YYYY-MM-DD,
                "title": title_string,
                "provider": provider_string,
                "rev": revenue_string,
                "time": time_string HH:MM
            }
            Data has been checked prior to calling function. Ideally there would be checks here in this function
            was used elsewhere.
    :return:
    """
    box_id = new_data['stb']
    date = new_data['date']
    title = new_data['title']
    provider = new_data['provider']
    rev = new_data['rev']
    time = new_data['time']

    try:
        os.makedirs(DIR)
    except FileExistsError:
        pass
    filename = os.path.normpath(DIR + '/' + box_id + '.json')

    try:
        with open(filename, 'r') as data_file:
            existing_data = json.load(data_file)
    except IOError:
        existing_data = {'stb': box_id}

    if date not in existing_data:
        existing_data[date] = {}

    existing_data[date][title] = {'rev': rev, 'time': time, 'provider': provider}

    with open(filename, 'w') as data_file:
        json.dump(existing_data, data_file)

    # Update index files
    create_indices(new_data)
    return


def get_filtered_stb(filter_by):
    """
    Return set of STB ids based on the filter.
    :param filter_by: Key, Value pair for the filter in a tuple:
                ( 'filter', 'value' )
    :return: set of STB ids matching filter
    """
    result = None

    # If there are no filters, return all STB ids.
    # This would would eventually cause problems when data-store gets too large
    if not filter_by:
        result = set()
        for file in os.listdir(DIR):
            if file.startswith('stb'):
                result.add(file.split('.')[0])
    # If filter is just the STB id, then simply return the STB id.
    elif 'stb' == filter_by[0]:
        result = {filter_by[1]}
    # Else find matching STB ids for filter from index files.
    else:
        key, value = filter_by
        filename = os.path.normpath(DIR + '/' + key + '_index.json')
        with open(filename, 'r') as index_file:
            index_data = json.load(index_file)
        try:
            result = set(index_data[value])
        # If there is no data matching the filter, return nothing.
        except KeyError:
            return set()
    return result


def selected(data, select):
    """
    Takes data and removes any values/columns not in SELECT parameter
    :param data: List of data entries to be SELECT'ed. ex:
                [
                    { 'stb': 'stb1',
                      'title': 'the matrix',
                      'rev': '6.00',
                      'date': '2017-05-01',
                      'provider': 'Warner Brothers',
                      'time': '12:30' },
                    { ... }
                ]
    :param select: List of SELECT parameters. ex: ['stb', 'rev', 'title']
    :return: List of data with only keys matching SELECT parameters
    """
    result = []
    for entry in data:
        result += [{key: entry[key] for key in select}]

    return result


def get_data_matching_filter(filter_by, raw_data):
    """
    Returns a list of data matching filter_by from a given STB's raw_data
    :param filter_by: Tuple containing (filter_name, filter_value)
    :param raw_data: Dictionary of raw stb_data for 1 STB.
    :return: List of dictionary entries from flattened STB matching filter.
    """
    result = []
    # If there is no filter, then return all data from this STB.
    filter_name, filter_value = filter_by if filter_by else ('stb', raw_data['stb'])

    # Flatten the data structure and filter desired results
    for date in (keys for keys in raw_data if keys not in ['stb']):
        for title in raw_data[date]:
            entry = {
                'stb': raw_data['stb'],
                'date': date,
                'title': title,
                'provider': raw_data[date][title]['provider'],
                'rev': raw_data[date][title]['rev'],
                'time': raw_data[date][title]['time']
            }
            # If the entry matches the filter, add flattened data to the result list
            result += [entry] if entry[filter_name] == filter_value else []

    return result


def get_data(stb_ids, select, filter_by, order):
    """
    Gets a list of filtered, selected, and ordered data.
    :param stb_ids: set of STB ids. ex: {'stb1', 'stb3', 'stb6'}
    :param select: List of SELECT parameters. ex: ['stb', 'title', 'rev']
    :param filter_by: tuple of filter and value ex: ('title', 'the matrix')
    :param order: list of column names to order ex: [ 'rev', 'title', 'stb' ]
    :return: list of filtered, selected, and ordered data.
                ex: [ {'stb': 'stb1', 'title': 'the matrix', 'rev': '6.00'}, ...]
    """
    filtered_data = []
    for stb_id in stb_ids:
        filename = os.path.normpath(DIR + '/' + stb_id + '.json')
        with open(filename, 'r') as data_file:
            raw_stb_data = json.load(data_file)
        filtered_data += get_data_matching_filter(filter_by, raw_stb_data)

    # Get just the SELECT data from the filtered data
    result = selected(filtered_data, select)
    # Order the data by ORDER
    result.sort(key=lambda x: tuple([x[y] for y in order])) if order else result

    return result
