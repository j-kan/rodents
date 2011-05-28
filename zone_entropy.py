#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv


import sys
import csv
import os
import glob
import re
from math  import log
from dicts import DefaultDict
from bigram import zones, bigrams, probs_bigrams, remove_self_transitions, h



def print_header():
  print ",".join(["Handling", "Rat", "Session", "Zone", "Entropy", "Between Zone Entropy", "Occupancy", "Out Transitions"])


def process_file(filename, handling, rat, session): 
  allzones = zones(filename)

  bi = bigrams(allzones)
  pp = probs_bigrams(bi)

  between_zone_bi = remove_self_transitions(bi)
  between_zone_pp = probs_bigrams(between_zone_bi)

  #print filename 

  for (zone, p) in pp.iteritems():
    entropy = h(p.values())
    count = sum(bi[zone].values())

    bz_p = between_zone_pp[zone]
    bz_entropy = h(bz_p.values())
    bz_count = sum(between_zone_bi[zone].values())

    #details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()])

    #print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
  
    print ','.join([handling, rat, session, zone, str(entropy), str(bz_entropy), str(count), str(bz_count)])

  #print "\tzone transitions:       %d" % total_count
  #print "\ttotal entropy:          %f" % total_entropy 
  #print "\tper-transition entropy: %f" % (total_entropy / total_count)


def main(argv=None):
  #root_dir = 'X36TrackDataS1S2-5-23-11'

  if argv is None:
      argv = sys.argv

  if len(argv) == 2:
      root_dir = argv[1]
   
      grepper = re.compile('^%s\/([en])r(\d+)s([12])\.csv$' % root_dir)

      print_header()

      for infile in glob.glob( '%s/*.csv' % root_dir):
        m = grepper.match(infile)
        if m:
          handling, rat, session = (m.group(1), m.group(2), m.group(3))
          process_file(infile, handling, rat, session)

  else:
    print "please specify a root directory"


if __name__ == '__main__':
    sys.exit(main())


