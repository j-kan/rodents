#! /usr/bin/env python

import sys
import csv
import re
import glob


USAGE = """

Translates raw CSVs with boolean zone indicators into CSVs 
with a single categorical 'Zone' column.

Usage: 
     %s <directory>
        
        where <directory> is a directory full of raw csvs, or

     %s < <filename>

        where <filename> is a single csv file.  
"""


FIRST_ZONE_COL = 6

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
    outrow = row[0:FIRST_ZONE_COL] + zone
    outstream.write(','.join(outrow))
    outstream.write('\n')



def process_all_files(root_dir):
  """Translate all files in a directory"""

  #root_dir = 'X36TrackDataS1S2-5-23-11'
  grepper = re.compile('^%s\/X36-([en])h-T\d\dr(\d+)s([12])\.csv$' % root_dir)
  
  for infile in glob.glob( '%s/X36-*.csv' % root_dir):
    print infile
    m = grepper.match(infile)
    if m:
      handling, rat, session = (m.group(1), m.group(2), m.group(3))
      with open(infile, 'r') as f:
        with open("%s/%sr%ss%s.csv" % (root_dir, handling.lower(), rat, session), 'w') as of:
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

    
    

