#! /usr/bin/env python

import sys
import csv
import os
import glob
import re
 


first = True

def process_file(filename, handling, rat, session): 
  global first

  with open(filename, 'r') as f: 
    reader = csv.reader(f) 
    infields = reader.next()
    outfields = infields + ['Handling', 'Rat', 'Session']
    
    if first: 
      print ','.join(outfields)
      first = False

    for row in reader: 
      outrow = row + [handling, "R" + rat, "S" + session]
      print ','.join(outrow)



def main(argv=None):
  grepper = re.compile('^z([en])r(\d+)s([12])\.csv$')

  for infile in glob.glob( 'z*.csv'):
    m = grepper.match(infile)
    if m:
      handling, rat, session = (m.group(1), m.group(2), m.group(3))
      process_file(infile, handling, rat, session)




if __name__ == '__main__':
    sys.exit(main())


