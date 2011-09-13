#! /usr/bin/env python

# usage: ./within_session_entropy.py X36TrackDataS1S2-5-23-11 > wse.csv


import sys
import csv
import directory_search
from math  import log
from dicts import DefaultDict
from bigram import zones_by_epoch, distance_by_epoch, unigrams, bigrams, probs, probs_bigrams, remove_self_transitions, h



def print_header():
  print ",".join(["Treatment", "Rat", "Session", "Epoch", "Observations", 
                  "Distance", "Entropy", "Cond Entropy", 
                  "X Zone Transitions", "X Zone Cond Entropy"])


def process_file(filename, treatment, rat, session, num_epochs, print_dict=False): 
  allzones_by_epoch = zones_by_epoch(filename,3)
  distances_by_epoch = distance_by_epoch(filename,3)

  for epoch, (ezones, edist) in enumerate(zip(allzones_by_epoch, distances_by_epoch)):
    unigram_counts  = unigrams(ezones)
    unigram_probs   = probs(unigram_counts)
    unigram_entropy = h(unigram_probs.values())

    bigram_counts = bigrams(ezones)
    bigram_probs  = probs_bigrams(bigram_counts)

    between_zone_bi = remove_self_transitions(bigram_counts)
    between_zone_pp = probs_bigrams(between_zone_bi)

    total_count = 0
    total_entropy = 0
    total_between_zone_count = 0
    total_between_zone_entropy = 0

    for (p, zone) in bigram_probs.sorted():
      entropy = h(p.values())
      count   = unigram_counts[zone]

      total_count = total_count + count
      total_entropy = total_entropy + (count * entropy)

      bz_p = between_zone_pp[zone]
      bz_entropy = h(bz_p.values())
      bz_count = sum(between_zone_bi[zone].values()) 
      
      total_between_zone_count   = total_between_zone_count + bz_count 
      total_between_zone_entropy = total_between_zone_entropy + (bz_count * bz_entropy)

      if print_dict:
        details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()])
        print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
      
    bigram_entropy    = total_entropy / total_count
    bigram_bz_entropy = total_between_zone_entropy / total_between_zone_count

    print ','.join(
      [str(x) for x in [treatment, rat, session, epoch, total_count, 
                        edist, unigram_entropy, bigram_entropy, 
                        total_between_zone_count, bigram_bz_entropy]])
   

def main(argv=None):
  #root_dir = 'X36TrackDataS1S2-5-23-11'
  print_header()

  for (infile, treatment, rat, session) in directory_search.main(argv): 
    process_file(infile, treatment, rat, session, 3)


if __name__ == '__main__':
    sys.exit(main())


