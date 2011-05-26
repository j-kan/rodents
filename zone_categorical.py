#! /usr/bin/env python

import sys
import csv
import re
import glob


def process_stream(stream, outstream): 
  """translate boolean zone indicators into a 'Zone' categorical variable"""
  reader = csv.reader(stream) 
  infields = reader.next()
  outfields = infields[0:6] + ['Zone']
  outstream.write(','.join(outfields))
  outstream.write('\n')

  for row in reader: 
    zone = [field.split(' ')[1] for (field,val) in zip(infields[6:], row[6:]) if val == "1"]
    outrow = row[0:6] + zone
    outstream.write(','.join(outrow))
    outstream.write('\n')



def process_all_files():
  ROOT_DIR = 'X36TrackDataS1S2-5-23-11'
  grepper = re.compile('^%s\/X36-([en])h-T\d\dr(\d+)s([12])\.csv$' % ROOT_DIR)
  
  for infile in glob.glob( '%s/X36-*.csv' % ROOT_DIR):
    print infile
    m = grepper.match(infile)
    if m:
      handling, rat, session = (m.group(1), m.group(2), m.group(3))
      with open(infile, 'r') as f:
        with open("%s/%sr%ss%s.csv" % (ROOT_DIR, handling.lower(), rat, session), 'w') as of:
          process_stream(f, of)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    if not sys.stdin.isatty():
      process_stream(sys.stdin, sys.stdout)
    elif len(argv) < 2:
      process_all_files()
    else:
      with open(argv[1], 'r') as f: 
        process_stream(f, sys.stdout)
    


if __name__ == '__main__':
    sys.exit(main())

    
    

