#! /usr/bin/env python

# usage: ./bigram.py X36TrackDataS1S2-5-23-11 > entropy.csv
#        ./bigram.py X36TrackDataS12345_060111_Dani > s4-t-entropy.csv


import sys
import csv
import directory_search
from math  import log,sqrt
from dicts import DefaultDict
from itertools import groupby


X_COL    = 1
Y_COL    = 2



def unigrams(words):
    """Given an array of words, returns a dictionary containing occurrence counts of each word."""
    d = DefaultDict(0)
    for w in words:
        d[w] += 1
    return d

def bigrams(words):
    """Given an array of words, returns a dictionary of dictionaries,
    containing occurrence counts of bigrams."""
    d = DefaultDict(DefaultDict(0))
    for (w1, w2) in zip(words, words[1:]+[None]):
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


LOG2 = log(2)

def log2(x):
    return log(x)/LOG2


def h(p):
    """calculate the entropy of a probability distribution,
       represented as list of probabilities""" 

    return reduce(lambda a,b: a+b, [-x*log(x)/log(2) for x in p])
    


def sum_x_log_x(values):
    return sum( [x * log2(x) for x in values])


#return log2(c_sum) - sum( [ci * log2(ci) for ci in counts.values()])/c_sum

def unigram_h(words):
    c_sum  = len(words)
    counts = unigrams(words)
    return log2(c_sum) - sum_x_log_x(counts.values())/c_sum



def bigram_h(words):
    c_sum  = len(words)
    u_counts = unigrams(words)
    b_counts = bigrams(words)
    u_h = log2(c_sum) - sum( [ci * log2(ci) for ci in u_counts.values()])/c_sum
    subsum = sum([ sum_x_log_x(d.values()) for (zone, d) in b_counts.iteritems()])
    return (sum_x_log_x(u_counts.values()) - subsum)/c_sum




def get_column_index(name, headers):
  return next(i for i in xrange(len(headers)) if headers[i].startswith(name))


def zones(filename):
  """retrieve the zone sequence from a csv file"""
  with open(filename, 'r') as f: 
    reader = csv.reader(f) 
    zone_column = get_column_index('Zone', reader.next())
    
    return [row[zone_column] for row in reader] 


def zones_by_epoch(filename, num_epochs):
  """retrieve the zone sequence from a csv file, splitting up into a number of epochs"""

  def zones_with_epoch():
    with open(filename, 'r') as f: 
      reader = csv.reader(f) 
      headers = reader.next()
      time_column = get_column_index('Time', headers)
      zone_column = get_column_index('Zone', headers)

      return [(int (float(row[time_column]) // (1800/num_epochs)), row[zone_column]) for row in reader] 

  return [[v for (k,v) in group] for key, group in groupby(zones_with_epoch(), lambda x: x[0])]
    


def xy(filename):
  """retrieve x,y positions from a csv file"""
  with open(filename, 'r') as f: 
    reader = csv.reader(f) 
    reader.next()
    return [(int(row[X_COL]),int(row[Y_COL])) for row in reader if row[X_COL] != '' and row[Y_COL] != ''] 


def euclidean_distance((x2,y2),(x1,y1)):
  def square(x):
    return x*x
  return sqrt(square(x2-x1) + square(y2-y1))


def total_distance(pos): 
  return sum([euclidean_distance(p2, p1) for [p2,p1] in zip(pos[1:], pos[0:len(pos)-1])])



#def distance_by_epoch(filename, num_epochs):
  #"""retrieve the distance traveled from a csv file, splitting up into a number of epochs"""

  #def zones_with_epoch():
    #with open(filename, 'r') as f: 
      #reader = csv.reader(f) 
      #reader.next()
      #return [(int (float(row[TIME_COL]) // (1800/num_epochs)), row[ZONE_COL]) for row in reader] 

  #return [[v for (k,v) in group] for key, group in groupby(zones_with_epoch(), lambda x: x[0])]
    

def print_header():
  print ",".join(["Treatment", "Rat", "Session", "Distance", "Observations",
                  "Entropy", "Cond Entropy", "Sum Entropy", "Unweighted Sum Entropy", 
                  "X Zone Cond Entropy", "X Zone Transitions", "X Zone Sum Entropy", "X Zone Unweighted Entropy"])


def process_file(filename, handling, rat, session, print_dicts=False): 
  """prints one row per file containing all calculated statistics"""

  allzones = zones(filename)
  distance = total_distance(xy(filename))

  
  unigram_counts = unigrams(allzones)
  unigram_probs  = probs(unigram_counts)
  unigram_entropy = h(unigram_probs.values())

  u_h = unigram_h(allzones)

  bigram_counts = bigrams(allzones)
  bigram_probs  = probs_bigrams(bigram_counts)

  b_h = bigram_h(allzones)

  between_zone_bigram_counts = remove_self_transitions(bigram_counts)
  between_zone_bigram_probs  = probs_bigrams(between_zone_bigram_counts)

  #print filename 

  total_count = 0
  total_entropy = 0
  total_unweighted_entropy = 0
  total_between_zone_count = 0
  total_between_zone_entropy = 0
  total_between_zone_unweighted_entropy = 0

  for (p, zone) in bigram_probs.sorted():

    entropy = h(p.values())                     # H( W_t+1 | W_t = z_i )
    count   = unigram_counts[zone]              # N_i

    #count2 = sum(bigram_counts[zone].values())

    #if count != count2:
      #print "?????: %4s %4d vs %4d" % (zone, count, count2)

    total_count = total_count + count
    total_unweighted_entropy = total_unweighted_entropy + entropy
    total_entropy = total_entropy + (count * entropy)

    bz_p = between_zone_bigram_probs[zone]
    bz_entropy = h(bz_p.values())
    bz_count = sum(between_zone_bigram_counts[zone].values())

    total_between_zone_count              = total_between_zone_count + bz_count
    total_between_zone_unweighted_entropy = total_between_zone_unweighted_entropy + bz_entropy
    total_between_zone_entropy            = total_between_zone_entropy + (bz_count * bz_entropy)
    
    if print_dicts: 
      details = ' '.join([ "%4s:%f" % pair for pair in p.iteritems()]) 
      print "\t%4s : %4d * %f -> %4s" % (zone, count, entropy, details)
  

  bigram_entropy = total_entropy / total_count
  bigram_bz_entropy = total_between_zone_entropy / total_between_zone_count

  print ','.join(
      [str(x) for x in [handling, rat, session, distance, len(allzones),
                        unigram_entropy, bigram_entropy,  total_entropy, total_unweighted_entropy, 
                        bigram_bz_entropy, total_between_zone_count, total_between_zone_entropy, total_between_zone_unweighted_entropy]])

      #[str(x) for x in [handling, rat, session, 
                        #unigram_entropy, u_h, sum(unigram_counts.values()),
                        #bigram_entropy,  b_h]])

      
  #print "\tzone transitions:       %d" % total_count
  #print "\ttotal entropy:          %f" % total_entropy 
  #print "\tper-transition entropy: %f" % (total_entropy / total_count)


def main(argv=None):

  print_header()

  for (infile, handling, rat, session) in directory_search.main(argv): 
    process_file(infile, handling, rat, session, False)


if __name__ == '__main__':
    sys.exit(main())


