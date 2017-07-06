def card_ranks(hand):
    """
    """
    # dict mapping
    ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse=True)
    # what to change
    # return ranks
    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    """
    for i in range(1, len(ranks)):
        if ranks[i-1] - ranks[i] != 1:
            return False
    return True
    """
    return (max(ranks) - min(ranks)) == 4 and len(set(ranks)) == 5

def flush(hand):
    "Return True if all the cards have the same suit."
    """
    suits = [s for r,s in hand]
    a_suit = suits[0]
    for suit in suits[1:]:
        if a_suit != suit:
            return False
    return True
    """
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    """
    stat = dict()
    for rank in ranks:
        if rank in stat:
            stat[rank] += 1
        else:
            stat[rank] = 1

    for key, value in stat.items():
        if value == n:
            return key
    """
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    """
    first_pair = kind(2, ranks)
    if not first_pair: return None
    ranks.remove(first_pair)
    second_pair = kind(2, ranks)
    if first_pair and second_pair:
        return (max(first_pair, second_pair), min(first_pair, second_pair))
    else:
        return None
    """
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and pair != lowpair:
        return (pair, lowpair)
    else:
        return None

def poker(hands):
    "Return a list of winning hand: poker([hand,...]) => [hands]"
    # handle ties!!!
    return allmax(hands, key=hand_rank_new)


def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result


def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house, repeat myself
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)


def hand_rank_new(hand):
    groups = group(card_ranks(hand))
    counts, ranks = unzip(groups)
    # partition of an integer
    """
    return (9 if (5,) == counts else
            8 if straight(ranks) and flush(hand) else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if flush(hand) else
            4 if straight(ranks) else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks
    """
    return max(count_rankings[counts], 4 * straight(ranks) + 5 * flush(hand)), ranks

count_rankings = {(5,):10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3, (2, 2, 1):2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}


def group(items):
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    return zip(*pairs)


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5S 5D 9H 9C 6S".split() # Two pairs

    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight

    ah = "AS 2S 5C 6S 7C".split() # A high
    sh = "2C 3H 4C 6S 7C".split() # 7 high

    assert poker([s1, ah]) == [s1]
    assert poker([s1, s2, ah, sh]) == [s2]

    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 9, 8, 9, 6]) == False

    assert flush(sf) == True
    assert flush(fk) == False

    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(tpranks) == (9, 5)
    assert two_pair(sf) == None

    return 'tests pass'
