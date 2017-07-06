import random

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

"""
Bad shuffle: O(N * N)
"""
def swap(deck, i, j):
    deck[i], deck[j] = deck[j], deck[i]

def shuffle(deck):
    N = len(deck)
    for i in range(N - 1): # redundant one more operation
        swap(deck, i, random.randrange(i, N))

def shuffle1(deck):
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        swap(deck, i, j)

def shuffle2(deck):
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = True
        swap(deck, i, j)

def shuffle3(deck):
    N = len(deck)
    for i in range(N):
        swap(deck, i, random.randrange(N))

#################

# test permutation
from collections import defaultdict

def test_shuffler(shuffler, deck='abcd', n=100000):
    counts = defaultdict(int)
    for _ in range(n):
        input = list(deck)
        shuffler(input)
        counts[''.join(input)] += 1

    e = n*1./factorial(len(deck))
    ok = all((0.9 <= counts[item]/e <= 1.1 for item in counts))
    name = shuffler.__name__
    print '%s(%s) %s' % (name, deck, ('ok' if ok else '*** Bad ***'))
    print '   ',
    for item, count in sorted(counts.items()):
        print "%s:%4.1f" % (item, count * 100./n),
    print

def factorial(n): return 1 if (n <= 1) else n * factorial(n - 1)

def test_shufflers(shufflers=[shuffle, shuffle1], decks=['abcd']):
    for deck in decks:
        print
        for f in shufflers:
            test_shuffler(f, deck)

test_shufflers([shuffle, shuffle1, shuffle2, shuffle3])

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    result = []
    for i in range(numhands):
        result.append(deck[n*i:n*(i+1)])
    return result

from poker import hand_rank

hand_names = {0: 'High Card',
              1: 'Pair',
              2: '2 Pair',
              3: '3 Kind',
              4: 'Straight',
              5: 'Flush',
              6: 'Full House',
              7: '4 Kind',
              8: 'Straight Flush'}

def hand_percentages(n=1000000):
    counts = [0] * 9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1

    for i in reversed(range(9)):
        print "%14s: %6.3f %%" % (hand_names[i], 100. * counts[i]/n)

# hand_percentages()
