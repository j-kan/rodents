#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv


import sys
import csv
import directory_search
from math  import log
from dicts import DefaultDict
from itertools import groupby


ZONE_COL = 3
TIME_COL = 0

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


def zones_by_epoch(filename, num_epochs):
  """retrieve the zone sequence from a csv file, splitting up into a number of epochs"""

  def zones_with_epoch():
    with open(filename, 'r') as f: 
      reader = csv.reader(f) 
      reader.next()
      return [(int (float(row[TIME_COL]) // (1800/num_epochs)), row[ZONE_COL]) for row in reader] 

  return [[v for (k,v) in group] for key, group in groupby(zones_with_epoch(), lambda x: x[0])]
    


#def distance_by_epoch(filename, num_epochs):
  #"""retrieve the distance traveled from a csv file, splitting up into a number of epochs"""

  #def zones_with_epoch():
    #with open(filename, 'r') as f: 
      #reader = csv.reader(f) 
      #reader.next()
      #return [(int (float(row[TIME_COL]) // (1800/num_epochs)), row[ZONE_COL]) for row in reader] 

  #return [[v for (k,v) in group] for key, group in groupby(zones_with_epoch(), lambda x: x[0])]
    

def print_header():
  print ",".join(["Handling", "Rat", "Session", "Zone Transitions", "Entropy", "Unweighted Entropy", "Between Zone Transitions", "Between Zone Entropy", "Between Zone Unweighted Entropy"])


def process_file(filename, handling, rat, session, print_dicts=False): 
  allzones = zones(filename)

  bi = bigrams(allzones)
  pp = probs_bigrams(bi)

  between_zone_bi = remove_self_transitions(bi)
  between_zone_pp = probs_bigrams(between_zone_bi)

  #print filename 

  total_count = 0
  total_entropy = 0
  total_unweighted_entropy = 0
  between_zone_count = 0
  between_zone_entropy = 0
  between_zone_unweighted_entropy = 0

  for (p, zone) in pp.sorted():
    entropy = h(p.values())
    count = sum(bi[zone].values())

    total_count = total_count + count
    total_unweighted_entropy = total_unweighted_entropy + entropy
    total_entropy = total_entropy + (count * entropy)

    bz_p = between_zone_pp[zone]
    bz_entropy = h(bz_p.values())
    bz_count = sum(between_zone_bi[zone].values())

    between_zone_count = between_zone_count + bz_count
    between_zone_unweighted_entropy = between_zone_unweighted_entropy + bz_entropy
    between_zone_entropy = between_zone_entropy + (bz_count * bz_entropy)
    
    if print_dicts: 
      details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()]) 
      print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
  
  print ','.join(
      [str(x) for x in [handling, rat, session, 
                        total_count, total_entropy, total_unweighted_entropy, 
                        between_zone_count, between_zone_entropy, between_zone_unweighted_entropy]])

  #print "\tzone transitions:       %d" % total_count
  #print "\ttotal entropy:          %f" % total_entropy 
  #print "\tper-transition entropy: %f" % (total_entropy / total_count)


def main(argv=None):

  print_header()

  for (infile, handling, rat, session) in directory_search.main(argv): 
    process_file(infile, handling, rat, session)


if __name__ == '__main__':
    sys.exit(main())


