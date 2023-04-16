"""Utils for generating CLI strings."""

import collections

from src.game import gem_utils
from src.game import player_game_state
from src.proto.gem_proto import GemType
from src.proto.deck_proto import Deck


THICK_SEPARATOR = "\n===========================\n"
THIN_SEPARATOR = "\n-------------------------\n"


def GemTypeToSymbol(gem_type):
  if gem_type == GemType.BLUE:
    return "Bl"
  elif gem_type == GemType.GREEN:
    return "Gr"
  elif gem_type == GemType.RED:
    return "R"
  elif gem_type == GemType.WHITE:
    return "W"
  elif gem_type == GemType.BROWN:
    return "Br"
  elif gem_type == GemType.GOLD:
    return "Go"
  else:
    raise ValueError("No CLI shorthand for given GemType")


def DeckAsString(deck):
  if deck == Deck.LEVEL_1:
    return "I"
  elif deck == Deck.LEVEL_2:
    return "II"
  elif deck == Deck.LEVEL_3:
    return "III"
  else:
    raise ValueError("No CLI string for given Deck")


def GemsAsString(gems, separator="\n"):
  items = []
  for gem_type, count in gems.items():
    items.append(GemTypeToSymbol(gem_type) + ":" + str(count))
  msg = "  ".join(items)
  return msg


def CardsListAsString(cards):
  msg = ""
  for card in cards:
    msg += "{"
    msg += ("(" + str(card.points) + "|" +
            GemTypeToSymbol(card.gem) + "|" +
            card.asset_id + ") ")
    msg += "["
    msg += GemsAsString(card.cost, separator="  ")
    msg += "]"
    msg += "}\n"
  return msg


def CardsByDeckAsString(cards_by_deck, game_rules):
  revealed_cards = player_game_state.GetRevealedCards(
      cards_by_deck, game_rules)
  msg = ""
  for deck, cards in revealed_cards.items():
    msg += DeckAsString(deck) + ": "
    num_cards_left = len(cards_by_deck[deck]) - len(revealed_cards[deck])
    msg += "[" + str(num_cards_left) + "] "
    msg += "\n"
    msg += CardsListAsString(cards) + "\n"
  return msg

def NoblesAsString(noble_tiles):
  msg = ""
  for noble_tile in noble_tiles:
    msg += "{(" + str(noble_tile.points) + "|" + noble_tile.asset_id + ") ["
    msg += GemsAsString(noble_tile.gem_type_requirements, separator="  ")
    msg += "]}\n"
  return msg
