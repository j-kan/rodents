#! /usr/bin/env python

import sys
import csv


def process_stream(stream): 
  """only keep rows where the zone changes"""

  reader = csv.reader(stream) 
  fields = reader.next()
  zi = fields.index("Zone")
  print ','.join(fields)

  prevzone = ''

  for row in reader: 
    zone = row[zi]
    if zone != prevzone: 
      print ','.join(row)
      prevzone = zone



def main(argv=None):
    if argv is None:
        argv = sys.argv

    if not sys.stdin.isatty():
      process_stream(sys.stdin)
    else: 
      with open(argv[1], 'r') as f: 
        process_stream(f)
    


if __name__ == '__main__':
    sys.exit(main())

    
    

