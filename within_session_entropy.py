#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv


import sys
import csv
import directory_search
from math  import log
from dicts import DefaultDict
from bigram import zones_by_epoch, bigrams, probs_bigrams, remove_self_transitions, h



def print_header():
  print ",".join(["Handling", "Rat", "Session", "Epoch", "Zone Transitions", "Entropy", "Between Zone Transitions", "Between Zone Entropy"])


def process_file(filename, handling, rat, session, print_dict=False): 
  allzones_by_epoch = zones_by_epoch(filename,3)

  for epoch, ezones in enumerate(allzones_by_epoch):
    bi = bigrams(ezones)
    pp = probs_bigrams(bi)

    between_zone_bi = remove_self_transitions(bi)
    between_zone_pp = probs_bigrams(between_zone_bi)

    total_count = 0
    total_entropy = 0
    between_zone_count = 0
    between_zone_entropy = 0

    for (p, zone) in pp.sorted():
      entropy = h(p.values())
      count = sum(bi[zone].values())

      total_count = total_count + count
      total_entropy = total_entropy + (count * entropy)

      bz_p = between_zone_pp[zone]
      bz_entropy = h(bz_p.values())
      bz_count = sum(between_zone_bi[zone].values())

      between_zone_count = between_zone_count + bz_count
      between_zone_entropy = between_zone_entropy + (bz_count * bz_entropy)
      
      if print_dict:
        details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()])
        print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
      
    print ','.join(
      [str(x) for x in [handling, rat, session, epoch, total_count, total_entropy, between_zone_count, between_zone_entropy]])
   

def main(argv=None):
  #root_dir = 'X36TrackDataS1S2-5-23-11'
  print_header()

  for (infile, handling, rat, session) in directory_search.main(argv): 
    process_file(infile, handling, rat, session)


if __name__ == '__main__':
    sys.exit(main())


