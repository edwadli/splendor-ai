"""Utils for generating CLI strings."""

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


def GemsAsString(gems_list):
  msg = ""
  gem_counts = gem_utils.CountGems(gems_list)
  for gem_type, count in gem_counts.iteritems():
    msg += GemTypeToSymbol(gem_type) + ": " + str(count) + "\n"
  return msg


def CardsListAsString(cards):
  msg = ""
  for card in cards:
    msg += str(card) + ";"
  return msg


def CardsByDeckAsString(cards_by_deck, game_rules):
  revealed_cards = player_game_state.GetRevealedCards(
      cards_by_deck, game_rules)
  msg = ""
  for deck, cards in revealed_cards.iteritems():
    msg += DeckAsString(deck) + ": "
    if len(revealed_cards[deck]) > 0:
      msg += "[] "
    else:
      msg += "   "
    msg += CardsListAsString(cards) + "\n"
  return msg
