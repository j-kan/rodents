import sys


def simple_cost(item1, item2):
    "The standard Levenstein cost function"
    if item1 == item2:
        return 0
    else:
        return 1

def simple_cost_x10(item1, item2):
    "The standard Levenstein cost function * 10"
    if item1 == item2:
        return 0
    else:
        return 10


def argmin(*a):
    "Returns: (the minimum value, its position in the argument list)"
    minval = sys.maxint
    position = -1

    for i, val in enumerate(a):
        if val < minval:
            minval = val
            position = i

    return (minval, position)


class AffineGap(object):

    "Calculates the affine-gap distance of two strings (or lists, or whatever)"

    def __init__(self, a, b, cost_fn=simple_cost, trace=True):
        self.a = a            # gap opening cost
        self.b = b            # gap continuing cost
        self.trace = trace
        self.cost_fn = cost_fn
        self.__a_very_big_number = 100000
                              # we use this as an "infinite" value:
                              #   not all values in the dynamic programming
                              #   table(s) are defined, so we assign those
                              #   spaces this value to mark them as "don't care"
                              #   cases.  Since we're always finding the minimum
                              #   value everywhere, these will never appear in
                              #   the final result.



    def __init_table(self):
        len1 = len(self.s1) # vertically
        len2 = len(self.s2) # horizontally

        # Allocate the table
        self.d   = [None]*(len2+1)
        self.dis = [None]*(len2+1)
        self.dit = [None]*(len2+1)

        if self.trace:
            self.trace_d   = [None]*(len2+1)
            self.trace_dis = [None]*(len2+1)
            self.trace_dit = [None]*(len2+1)

        for i in range(len2+1):
            self.d  [i] = [self.__a_very_big_number]*(len1+1)
            self.dis[i] = [self.__a_very_big_number]*(len1+1)
            self.dit[i] = [self.__a_very_big_number]*(len1+1)
            if self.trace:
                self.trace_d  [i] = [None]*(len1+1)
                self.trace_dis[i] = [None]*(len1+1)
                self.trace_dit[i] = [None]*(len1+1)

        # Initialize the table
        self.d  [0][0] = 0
        self.dis[1][0] = self.a
        self.dit[0][1] = self.a

        for i in range(2, len2+1):
            self.dis[i][0] = self.dis[i-1][0] + self.b
        for i in range(2, len1+1):
            self.dit[0][i] = self.dit[0][i-1] + self.b

        if self.trace:
            for i in range(1, len2+1):
                self.trace_dis[i][0] = 1
            for i in range(1, len1+1):
                self.trace_dit[0][i] = 2


    def __dynprog(self):
        len1 = len(self.s1) # vertically
        len2 = len(self.s2) # horizontally

        # Do dynamic programming
        for i in range(1, len2+1):
            for j in range(1, len1+1):
                self.d[i][j]   = self.cost_fn(self.s1[j-1], self.s2[i-1]) +    \
                                 min(  self.d  [i-1][j-1],
                                       self.dis[i-1][j-1],
                                       self.dit[i-1][j-1])
                self.dis[i][j] = min(
                                       self.d  [i-1][j] + self.a,
                                       self.dis[i-1][j] + self.b)
                self.dit[i][j] = min(
                                       self.d  [i][j-1] + self.a,
                                       self.dit[i][j-1] + self.b)
        self.__calc_total_distance()


    def __dynprog_with_tracing(self):
        """In this implementation each of the 3 separate tables represents a
           separate operation (copy, insert, and delete, respectively), so the
           trace_xxx tables store an index/'backpointer' which indicates which
           table will contain the next step in the backtrace.

           The 'trace_root' is the head of the resulting linked list"""

        len1 = len(self.s1) # vertically
        len2 = len(self.s2) # horizontally

        # Do dynamic programming
        for i in range(1, len2+1):
            for j in range(1, len1+1):
                self.d[i][j], self.trace_d[i][j] = \
                                argmin(self.d  [i-1][j-1],
                                       self.dis[i-1][j-1],
                                       self.dit[i-1][j-1])
                self.d[i][j] += self.cost_fn(self.s1[j-1], self.s2[i-1])

                self.dis[i][j], self.trace_dis[i][j] = \
                                argmin(self.d  [i-1][j] + self.a,
                                       self.dis[i-1][j] + self.b)
                self.dit[i][j], self.trace_dit[i][j] = \
                                argmin(self.d  [i][j-1] + self.a,
                                       sys.maxint,    # placeholder to make the indexing work out correctly
                                       self.dit[i][j-1] + self.b)
        self.__calc_total_distance()


    def __calc_total_distance(self):
        """calculates which of the 3 possible final values is the real final
           value, and records it"""

        len1 = len(self.s1) # vertically
        len2 = len(self.s2) # horizontally

        self.total_distance, self.trace_root = argmin(self.d  [len2][len1],
                                                      self.dis[len2][len1],
                                                      self.dit[len2][len1])


    def __trace_path(self):

        # names = ['d', 'dis', 'dit']

        i     = len(self.s2) # horizontally
        j     = len(self.s1) # vertically
        which = self.trace_root

        while i != 0 or j != 0:
            if which == 0:                    # d
                nexti = i-1
                nextj = j-1
                which = self.trace_d[i][j]
                self.trace_d[i][j] = "*"

            elif which == 1:                  # dis
                nexti = i-1
                nextj = j
                which = self.trace_dis[i][j]
                self.trace_dis[i][j] = "*"

            elif which == 2:                  # dit
                nexti = i
                nextj = j-1
                which = self.trace_dit[i][j]
                self.trace_dit[i][j] = "*"

            else:                             # huh?
                nexti = 0
                nextj = 0

            i = nexti
            j = nextj
            print "ij", i, j



    def distance(self, s1, s2, showtable=True):
        """The main entry point"""

        self.s1 = s1
        self.s2 = s2
        self.__init_table()

        if self.trace:
            self.__dynprog_with_tracing()
            self.__trace_path()
        else:
            self.__dynprog()

        if showtable:
            self.print_table()

        return self.total_distance



    def print_table(self):
        """Print the DP table, t, for strings s1 and s2.
           If the optional 'trace' is present, print * indicators for the alignment.
           Fancy formatting ensures this will also work when s1 and s2 are lists of strings"""
        print "              ",
        for i in range(len(self.s1)):
            print "%4.2s" % self.s1[i],
        print
        for i in range(len(self.d)):
            self.__print_row(i, 'd',   True)
            self.__print_row(i, 'dis')
            self.__print_row(i, 'dit')
            print


    def __print_row(self, i, field, show_char=None):
        table = getattr(self, field)
        if self.trace:
            tracetable = getattr(self, "trace_" + field)

        if show_char and i > 0:
            print "%3.3s" % self.s2[i-1],
        else:
            print '   ',

        print "  %3.3s" % field,

        for j in range(len(table[i])):
            if self.trace and tracetable[i][j] == "*":
                print " *" + "%2d" % table[i][j],
            elif table[i][j] >= self.__a_very_big_number:
                print "  --",    # this is a "not-a-number" or "don't care" value
            else:
                print "%4d" % table[i][j],
        print



def affine_gap_distance(s1, s2, showtable=True):
    """multiply everything by 10 to make use integer math"""
    ag = AffineGap(10, 1, simple_cost_x10)
    dist1 = ag.distance(s1, s2, showtable)/10.0
    print "affine gap: %f" % dist1


if __name__ == '__main__':
    affine_gap_distance("grunion", "run")
    affine_gap_distance("run", "grunion")
    affine_gap_distance("shakespeare", "park")
    affine_gap_distance(['this', 'is', 'a', 'test'], ['this', 'will', 'be', 'another', 'test'])
