"""Utils to parse a csv file for DevelopmentCard data."""

import collections
import csv

from src.proto.gem_proto import GemType
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard

def int_to_deck_level(level):
    if level == 1:
        return Deck.LEVEL_1
    elif level == 2:
        return Deck.LEVEL_2
    elif level == 3:
        return Deck.LEVEL_3
    else:
        raise ValueError("Data error (Deck level invalid)")


def str_to_gem(s):
    if s == 'BLUE':
        return GemType.BLUE
    elif s == 'GREEN':
        return GemType.GREEN
    elif s == 'RED':
        return GemType.RED
    elif s == 'WHITE':
        return GemType.WHITE
    elif s == 'BROWN':
        return GemType.BROWN
    else:
        raise ValueError("Data error (GemType invalid)")


def build_deck(file):
    '''Use a csv file to build a deck of development cards.'''
    deck = []
    with open(file, 'rt') as csv_file:
        card_data_reader = csv.DictReader(csv_file, delimiter=',')
        for row in card_data_reader:
            asset_id = row['asset_id']
            level = int_to_deck_level(int(row['level']))
            point = int(row['point'])
            gem = str_to_gem(row['gem'])
            cost = collections.Counter({
                GemType.BLUE: int(row['blue_cost']),
                GemType.GREEN: int(row['green_cost']),
                GemType.RED: int(row['red_cost']),
                GemType.WHITE: int(row['white_cost']),
                GemType.BROWN: int(row['brown_cost'])})
            deck.append(DevelopmentCard(
                asset_id=asset_id,
                level=level,
                points=point,
                gem=gem,
                cost=cost,))

    return deck
