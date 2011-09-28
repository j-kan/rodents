#! /usr/bin/env python

# usage: ./zone_entropy.py X36TrackDataS1S2-5-23-11 > h-per-zone.csv




import sys
import re
import csv
import directory_search
from math  import log
from dicts import DefaultDict
from bigram import zones, bigrams, probs_bigrams, remove_self_transitions, remove_terminal_transitions, h, find_impossible_transitions


ZONE_GRAPH_REGEX = re.compile('^([a-z][a-z0-9]) \-\- ([a-z][a-z0-9])\s*$')
 

def zone_graphs(filename):
  """retrieve the zone graph from a text file"""
  d   = DefaultDict(DefaultDict(0))
  bzd = DefaultDict(DefaultDict(0))
  with open(filename, 'r') as f: 
    for l in f.xreadlines():
      m = ZONE_GRAPH_REGEX.search(l)
      if m:
        src, dst = m.groups()
        d[src][dst]    = 1
        d[dst][src]    = 1
        d[src][src]    = 1
        d[dst][dst]    = 1
        bzd[src][dst]  = 1
        bzd[dst][src]  = 1
  return (d,bzd)


def uniform_zone_entropy(graph):
    pp = probs_bigrams(graph)
    return dict([(z, h(p.values())) for (z,p) in pp.iteritems()])
  

def print_header():
  print ",".join(["Treatment", "Rat", "Session", "Zone", 
                  "Entropy", "Baseline", "Info Gain", 
                  "X Zone Entropy", "X Zone Baseline", "X Zone Info Gain", 
                  "Occupancy", "Out Transitions"])


def process_file(filename, treatment, rat, session): 
  """prints out a variety of statistics for each zone"""

  zone_g, between_zone_g = zone_graphs("zone-graph.txt")

  baseline              = uniform_zone_entropy(zone_g)
  between_zone_baseline = uniform_zone_entropy(between_zone_g)

  allzones = zones(filename)

  bigram_counts = remove_terminal_transitions(bigrams(allzones))
  bigram_probs  = probs_bigrams(bigram_counts)

  between_zone_bigram_counts = remove_self_transitions(bigram_counts)
  between_zone_bigram_probs  = probs_bigrams(between_zone_bigram_counts)

  #print filename 

  for (zone, p) in bigram_probs.iteritems():

    zone_destinations = zone_g[zone].keys()

    #impossible_transitions = [(zone, z2, pr) for (z2, pr) in p.iteritems() if z2 not in zone_destinations]
    impossible_transitions = find_impossible_transitions(zone_g, zone, p)

    #if len(impossible_transitions) > 0:
      #print "impossible transitions: " , treatment, rat, session, impossible_transitions

    entropy = h(p.values())
    count   = sum(bigram_counts[zone].values())

    bz_p       = between_zone_bigram_probs[zone]
    bz_entropy = h(bz_p.values())
    bz_count   = sum(between_zone_bigram_counts[zone].values())

    #details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()])

    #print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
  
    print ','.join([str(x) for x in 
                    [treatment, rat, session, zone, 
                     entropy, baseline[zone], baseline[zone]-entropy,
                     bz_entropy, between_zone_baseline[zone], between_zone_baseline[zone]-bz_entropy, 
                     count, bz_count]])

  #print "\tzone transitions:       %d" % total_count
  #print "\ttotal entropy:          %f" % total_entropy 
  #print "\tper-transition entropy: %f" % (total_entropy / total_count)


def main(argv=None):
  #root_dir = 'X36TrackDataS1S2-5-23-11'
  print_header()

  for (infile, treatment, rat, session) in directory_search.main(argv): 
    process_file(infile, treatment, rat, session)


if __name__ == '__main__':
    sys.exit(main())


