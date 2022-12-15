from collections import defaultdict
from itertools import chain, combinations
from typing import Dict, FrozenSet, List

from utils import timer


def get_init_itemset(itemsets: List[List[int]]):
    """get_itemset

    Args:
        itemsets (list): The data to get the itemset from

    Returns:
        frequent 1-itemset
    """
    itemset = set()
    for row in itemsets:
        for item in row:
            itemset.add(frozenset([item]))

    return itemset


def get_frequent_itemset(
    itemset: FrozenSet,
    itemsets: List[List[int]],
    min_support: float,
    itemset_with_support: Dict[FrozenSet, int]
):

    frequent_itemset = set()
    local_support = defaultdict(int)

    for item in itemset:
        for tarset in itemsets:
            if item.issubset(tarset):
                itemset_with_support[item] += 1
                local_support[item] += 1

    for item, support in local_support.items():
        support = support / len(itemsets)
        if support >= min_support:
            frequent_itemset.add(item)

    return frequent_itemset


def get_self_joining(frequent_itemsets: List[FrozenSet]):
    """Get self-joining in k length"""

    # itemsets must be sorted
    indexing_sets = sorted(sorted(itemset) for itemset in frequent_itemsets)
    candidate_itemset = list()

    i = 0
    while i < len(indexing_sets):

        skip = 1
        first = indexing_sets[i][:-1]
        tails = [indexing_sets[i][-1]]
        for j in range(i+1, len(indexing_sets)):

            if first == indexing_sets[j][:-1]:
                tails.append(indexing_sets[j][-1])
                skip += 1
            else:
                break

        for a, b in sorted(combinations(tails, 2)):
            candidate_itemset.append(frozenset(first + [a, b]))

        i += skip

    return set(candidate_itemset)


def get_subsets(s: FrozenSet):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def ap_association_rules(
    frequent_itemsets: List[FrozenSet],
    itemsets_with_support: Dict[FrozenSet, int],
    min_confidence: float,
    len_set: int
):

    rules = list()
    for freq_k_itemset in frequent_itemsets:
        for freq_itemset in freq_k_itemset:

            subsets = get_subsets(freq_itemset)
            support = itemsets_with_support[freq_itemset]
            for subset in subsets:

                diff = set(freq_itemset) - set(subset)
                confidence = support / itemsets_with_support[frozenset(subset)]
                lift = confidence / itemsets_with_support[frozenset(diff)]
                if confidence >= min_confidence:
                    rules.append([
                        set(subset), set(diff),
                        support/len_set, confidence, lift*len_set
                    ])

    return rules


@timer
def apriori(itemsets: List[List], args):
    """Apriori algorithm

    Args:
        itemsets (list): The itemsets
        args: The arguments

    Returns:
        list of frequent itemsets
    """

    # TODO: efficient apriori algorithm, see:
    # https://github.com/tommyod/Efficient-Apriori/tree/master/efficient_apriori

    min_support = args.min_sup
    min_confidence = args.min_conf

    # global itemset
    frequent_itemsets = list()

    # create a dictionary of items and their support
    itemset_with_support = defaultdict(int)

    # get all unique items
    init_itemset = get_init_itemset(itemsets)

    # get all frequent 1-itemsets
    curr_itemset = get_frequent_itemset(init_itemset, itemsets, min_support, itemset_with_support)

    k = 2
    while len(curr_itemset) >= 1:

        frequent_itemsets.append(curr_itemset)

        # get pruned candidate itemsets
        candidate_itemset = get_self_joining(curr_itemset)

        # count support
        curr_itemset = get_frequent_itemset(candidate_itemset, itemsets, min_support, itemset_with_support)

        k += 1

    # get association rules
    rules = ap_association_rules(frequent_itemsets, itemset_with_support, min_confidence, len(itemsets))

    return rules