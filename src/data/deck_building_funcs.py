import sys
sys.path.append('C:/Users/erik.hou/Studies/Personal Projects/splendor-ai')

from src.proto.gem_proto import GemType
from src.proto.deck_proto import Deck
from src.proto.development_card_proto import DevelopmentCard

def int_to_deck_level(level):
    if level == 1:
        return Deck.LEVEL_1
    elif level == 2:
        return Deck.LEVEL_2
    else:
        return Deck.LEVEL_3

def str_to_gem(s):
    if s == 'BLUE':
        return GemType.BLUE
    elif s == 'GREEN':
        return GemType.GREEN
    elif s == 'RED':
        return GemType.RED
    elif s == 'WHITE':
        return GemType.WHITE
    else:
        return GemType.BROWN

def build_deck(file):
    
    '''use a file to build a deck of development cards'''
    
    f = open(file, 'rt')
    lines = f.readlines()
    f.close

    deck = []

    for i in range(1,len(lines)): #ignore the first line, headers
        line_list = lines[i].replace('\n', '').split(',')

        asset_id = line_list[0]
        level = int_to_deck_level(int(line_list[1]))
        point = line_list[2]
        gem = str_to_gem(line_list[3])

        cost = ([GemType.BLUE]*int(line_list[4]) +
                [GemType.GREEN]*int(line_list[5]) +
                [GemType.RED]*int(line_list[6]) +
                [GemType.WHITE]*int(line_list[7]) +
                [GemType.BROWN]*int(line_list[8]))

        deck.append(DevelopmentCard(
            asset_id=asset_id,
            level=level,
            points=point,
            gem=gem,
            cost=cost,))

    return deck
        
        
        