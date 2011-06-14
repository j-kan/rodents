#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv


import sys
import csv
import directory_search
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
  print_header()

  for (infile, handling, rat, session) in directory_search.main(argv): 
    process_file(infile, handling, rat, session)


if __name__ == '__main__':
    sys.exit(main())


