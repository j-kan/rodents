#! /usr/bin/env python

import re
import sys
import glob


def raw_csv_files(root_dir):
  """searches for raw track data csvs in a particular directory"""

  #grepper = re.compile('^%s\/X36TrackDataS(\d)\/X36-([en])h-T29r(\d+)s(\d)\.csv$' % root_dir) 
  grepper = re.compile('^%s\/X\d+-(\w+)-T\d+r(\d+)s(\d)\.csv$' % root_dir) 
  
  for infile in glob.glob( '%s/*.csv' % root_dir): 
    m = grepper.match(infile) 
    if m: 
      handling, rat, session = (m.group(1), m.group(2), m.group(3))
      #if session != m.group(4):
        #sys.stderr.write('session indicators do not match for: %s' % m.string) 
        
      outfile = "%s/%s-r%s-s%s.csv" % (root_dir, handling.lower(), rat, session)

      yield (infile, outfile)


def zone_csv_directory_search(root_dir):
  """searches for post-processed csvs (where appearance in a zone is a
     categorical attribute rather than a binary feature) in a particular
     directory, following the standard naming convention."""

  grepper = re.compile('^%s\/(\w+)-r(\d+)-s(\d)\.csv$' % root_dir)
  
  for infile in glob.glob( '%s/*.csv' % root_dir): 
    m = grepper.match(infile) 
    if m: 
      handling, rat, session = (m.group(1), m.group(2), m.group(3))
      yield (infile, handling, rat, session)

  
def main(argv=None):
  #root_dir = 'X36TrackDataS1S2-5-23-11'

  if argv is None:
      argv = sys.argv

  if len(argv) == 2:
      root_dir = argv[1]
      return zone_csv_directory_search(root_dir)

      #for (infile, handling, rat, session) in csv_directory_search(root_dir):
        #print "%s %s r=%s s=%s" % (infile, handling, rat, session)

  else:
    print "please specify a root directory"


if __name__ == '__main__':
    sys.exit(main())


  
