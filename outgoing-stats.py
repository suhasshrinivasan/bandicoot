"""Given a bandicoot metadata csv file,
provides outgoing statistics in time specified
time intervals.

IN : xyz.csv
OUT: Table of contents representing amount of 
outgoing call durations and sent sms texts in
given number_of_days.

Run instructions:
python outgoing-stats.py

NOTE: 
1. All paths are absolute.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# set window size: time intervals
time_interval = 30


# given records and index of records
# returns date at that index
# intermediately, converts datestring into date
# format of datestring: 'YYYY-MM-DD HH-MM-SS'
# format of date      : YYYY, MM, DD
def get_records_date(records, index):
    datestring = records.iloc[index].datetime.split(' ')[0]
    return datetime.strptime(datestring, '%Y-%m-%d').date()


# given records and index of records
# returns direction at that index
def get_records_direction(records, index):
    return records.iloc[index].direction


# given records and index of record
# returns interaction type at that index
def get_records_type(records, index):
    return records.iloc[index].interaction


# given records and index of records
# returns call_duration at that index
def get_records_call_dur(records, index):
    return records.iloc[index].call_duration


# given out_data_object is wrapped up with final entries
# out_data_list is appended with wrapped object
# new out_data_object is declared with start_data init
def wrap_and_init(out_data_object, out_data_list, current_date):
    out_data_object.end_date = current_date
    out_data_object.number_of_days = (current_date - out_data_object.start_date).days
    out_data_list.append(out_data_object)
    out_data_object = OutData()
    out_data_object.start_date = current_date
    return out_data_object, out_data_list


# OutData is a composite type consisting of stats data
class OutData(object):
    start_date = None
    end_date = None
    number_of_days = 0
    call_dur = 0
    nsms = 0

    def print_stats(self):
        print "Start date: " + str(self.start_date)
        print "End date: " + str(self.end_date)
        print "Number of days: " + str(self.number_of_days)
        print "Outgoing call duration: " + str(int(self.call_dur)) + "s | " + str(int(self.call_dur/60)) + "min | " + str(int(self.call_dur/60/time_interval)) + "min per day"
        print "Number of sms sent: " + str(self.nsms)


# main
def main():
    # load the records using pandas
    records = pd.read_csv('/home/suhas/Work/all-about-data/bandicoot/bob.csv')

    # declare a list for OutData objects
    out_data_list = []
    # declare an OutData object
    out_data_object = OutData()
    # init
    out_data_object.start_date = get_records_date(records, 0)
    # get number of records
    records_len = len(records)

    walker = 0
    while walker < records_len:

        current_date = get_records_date(records, walker)
        # while iterating through records
        # if number of days exceeds time_interval
        if (current_date - out_data_object.start_date).days >= time_interval:
            out_data_object, out_data_list = wrap_and_init(out_data_object, out_data_list, current_date)
            continue

        if get_records_direction(records, walker) == 'out':
            if get_records_type(records, walker) == 'call':
                if not np.isnan(get_records_call_dur(records, walker)):
                    out_data_object.call_dur += get_records_call_dur(records, walker)
            else:
                out_data_object.nsms += 1

        walker += 1

    out_data_object, out_data_list = wrap_and_init(out_data_object, out_data_list, current_date)
    del out_data_object

    for out_data_object in out_data_list:
        out_data_object.print_stats()
        print '\n'


if __name__ == '__main__':
    main()