#! /usr/bin/env python

# usage: ./forays.py X36TrackDataS1S2-5-23-11 > entropy.csv
#        ./forays.py X36TrackDataS12345_060111_Dani > s4-t-entropy.csv

import sys
import csv
from math  import log,sqrt
from dicts import DefaultDict
from itertools import groupby

import numpy

import directory_search
from bigram import zones

import affine_gap


X_COL    = 1
Y_COL    = 2


#def find_neighbors(target, interests, distancefinder, threshold=25):
    #t1 = time.time()
    #d = DefaultDict(0)
    #for candidate in interests.keys():
        #dist = distancefinder.distance(target, candidate, False)
        #if dist < threshold:
            #d[candidate] = dist
            #print candidate, ' ', dist
    #t2 = time.time()
    #print_neighbors(d, interests)
    #print "time elapsed (secs): ", t2-t1
    #return (d, t2-t1)


#def print_neighbors(d, interests, num=30):
    #subset = d.sorted(rev=False)[:num]
    #for distance, interest in subset:
        #print "%2d %20s  %d" % (distance, interest, interests[interest])


class AffineGap(affine_gap.AffineGap):

    """This is here to make the AffineGap and Levenshtein
       algorithms have the same interface"""

    def __init__(self):
        affine_gap.AffineGap.__init__(self, 10, 1, affine_gap.simple_cost_x10, False)
        self.threshold = 25

    #def neighbors(self, target, interests):
        #return find_neighbors(target, interests, self, self.threshold)


class Levenshtein(affine_gap.AffineGap):

    """This is here to make the AffineGap and Levenshtein
       algorithms have the same interface"""

    def __init__(self):
        affine_gap.AffineGap.__init__(self, 1, 1, affine_gap.simple_cost, False)
        self.threshold = 4

    # def distance(self, s1, s2, showtable=True):
    #     return stredit.stredit(s1, s2, showtable)

    #def neighbors(self, target, interests):
        #return find_neighbors(target, interests, self, self.threshold)

#def zones(filename):
  #"""retrieve the zone sequence from a csv file"""
  #with open(filename, 'r') as f:
    #print filename
    #reader = csv.reader(f)
    #zone_column = get_column_index('Zone', reader.next())

    #return [row[zone_column] for row in reader]

def forays(zones):
    one_foray = []
    for z in zones:
        if z in ['a0','a1']:
            if len(one_foray) > 0:
                yield(one_foray)
            one_foray = []
        else:
            one_foray.append(z)



def distance_matrix(filename, distance_finder, print_dicts=False):
  allforays = [f for f in forays(zones(filename))]
  nf = len(allforays)

  if print_dicts:
      print "%s: %d forays" % (filename, nf)

  #for f in allforays:
      #print '-'.join(f)

  distances = numpy.zeros((nf, nf))

  for i in range(0,nf-1):
      for j in range(i+1,nf):
          distances[i,j] = distance_finder.distance(allforays[i], allforays[j], False)

  if print_dicts:
      print type(distance_finder).__name__
      print distances

  return distances


AG = AffineGap()
LV = Levenshtein()


def main(argv=None):

  numpy.set_printoptions(linewidth=200)

  distance_matrices = {}
  for (infile, treatment, rat, session) in directory_search.main(argv):
    distance_matrices[(treatment, rat, session)] = distance_matrix(infile, LV)

  return distance_matrices



if __name__ == '__main__':
    sys.exit(main())


