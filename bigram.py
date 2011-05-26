#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv


import sys
import csv
import os
import glob
import re
from math  import log
from dicts import DefaultDict


ZONE_COL = 6

def bigrams(words):
    """Given an array of words, returns a dictionary of dictionaries,
    containing occurrence counts of bigrams."""
    d = DefaultDict(DefaultDict(0))
    for (w1, w2) in zip(['<S>'] + words, words + [None]):
        d[w1][w2] += 1
    return d


def probs(dict):
    """given a dictionary of counts, return a dict of probabilities"""
    sum = reduce(lambda x,y: x+y, dict.itervalues(), 0)
    p = DefaultDict(0)
    for (w, c) in dict.iteritems():
        p[w] = float(c)/sum
    return p

    
def probs_bigrams(dict):
    """given a dictionary of dictionaries of counts, 
       return a dict of dicts of bigram probabilities"""
    p = DefaultDict(DefaultDict(0))
    for (w, d) in dict.iteritems():
        p[w] = probs(d)
    return p


def remove_self_transition(zone, transitions): 
    return dict([(k,v) for (k,v) in transitions.iteritems() if k != zone])

def remove_self_transitions(allbigrams):
    return dict([(zone, remove_self_transition(zone, transitions)) for (zone, transitions) in allbigrams.iteritems()])


def h(p):
    """calculate the entropy of a probability distribution,
       represented as list of probabilities""" 

    return reduce(lambda a,b: a+b, [-x*log(x)/log(2) for x in p])
    
    

def zones(filename):
  """retrieve the zone sequence from a csv file"""
  with open(filename, 'r') as f: 
    reader = csv.reader(f) 
    reader.next()
    return [row[ZONE_COL] for row in reader] 


def print_header():
  print ",".join(["Handling", "Rat", "Session", "Zone Transitions", "Entropy", "Between Zone Transitions", "Between Zone Entropy"])


def process_file(filename, handling, rat, session): 
  allzones = zones(filename)

  bi = bigrams(allzones)
  pp = probs_bigrams(bi)

  between_zone_bi = remove_self_transitions(bi)
  between_zone_pp = probs_bigrams(between_zone_bi)

  #print filename 

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
     
    
    details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()])

    #print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
  
  print ','.join([handling, rat, session, str(total_count), str(total_entropy), str(between_zone_count), str(between_zone_entropy)])

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


