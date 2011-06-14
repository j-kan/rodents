#! /usr/bin/env python

import sys
import csv
import time
import directory_search


USAGE = """

Translates raw CSVs with boolean zone indicators into CSVs with a single
categorical 'Zone' column, and converts 'HH:MM:SS.SS'-formatted times into
seconds.

Usage: 
     %s <directory>
        
        where <directory> is a directory full of raw csvs, or

     %s < <filename>

        where <filename> is a single csv file.  
"""


FIRST_ZONE_COL = 3


def translate_time_format(strtime):

  """Translates 'HH:MM:SS.SS'-formatted times into seconds, 
     returning the result as a string."""

  if ':' in strtime:
    secs, fraction = strtime.split('.')
    ts = time.strptime(secs,"%H:%M:%S")
    seconds = ts.tm_sec + 60*ts.tm_min + 3600*ts.tm_hour
    return "%d.%s" % (seconds, fraction)
  else:
    return strtime



def process_stream(stream, outstream): 

  """Translate boolean zone indicators in a single csv file 
     into a 'Zone' categorical variable for each row"""

  reader = csv.reader(stream) 
  infields = reader.next()
  outfields = infields[0:FIRST_ZONE_COL] + ['Zone']
  outstream.write(','.join(outfields))
  outstream.write('\n')

  for row in reader: 
    zone = [field.split(' ')[1] for (field,val) in zip(infields[FIRST_ZONE_COL:], row[FIRST_ZONE_COL:]) if val == "1"]
    seconds = translate_time_format(row[0])
    outrow = [seconds] + row[1:FIRST_ZONE_COL] + zone
    outstream.write(','.join(outrow))
    outstream.write('\n')



def process_all_files(root_dir):

  """Translate all raw csv files in a directory to zone categorical files"""

  #root_dir = 'X36TrackDataS1S2-5-23-11'
  
  for (infile, outfile) in directory_search.raw_csv_files(root_dir):
    print infile
    with open(infile, 'r') as f: 
      with open(outfile, 'w') as of: 
        process_stream(f, of)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    if not sys.stdin.isatty():
      process_stream(sys.stdin, sys.stdout)
    elif len(argv) == 2:
      process_all_files(argv[1])
    else:
      print USAGE % (argv[0],argv[0])
      #with open(argv[1], 'r') as f: 
        #process_stream(f, sys.stdout)
    


if __name__ == '__main__':
    sys.exit(main())

    
    

