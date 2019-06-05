"""Utils for running the game."""

from src.proto.gem_proto import GemType
from src.game import gem_utils


def is_gems_taken_only_gold(player_action):
    gems = player_action.gems_taken
    gold_gem_count = gems[GemType.GOLD]
    return (gem_utils.AllZerosExcept(gems, GemType.GOLD) and
            (gold_gem_count == 0 or gold_gem_count == 1))


def is_reserved_revealed_card(player_action):
    return (is_gems_taken_only_gold(player_action) and
            player_action.purchased_card_id is None and
            player_action.reserved_card_id is not None and
            player_action.topdeck_level is None)


def is_reserved_top_deck(player_action):
    return (is_gems_taken_only_gold(player_action) and
            player_action.purchased_card_id is None and
            player_action.reserved_card_id is None and
            player_action.topdeck_level is not None)


def is_purchased_card(player_action):
    return (gem_utils.NumGems(player_action.gems_taken) == 0 and
            player_action.purchased_card_id is not None and
            player_action.reserved_card_id is None and
            player_action.topdeck_level is None)


def is_taking_different_gems(player_action):
    gems_taken = player_action.gems_taken
    gem_types = gem_utils.GetNonEmptyGemTypes(gems_taken)
    if len(gem_types) > 3:
        return False
    if GemType.GOLD in gem_types:
        return False
    if not all(gems_taken[gem_type] == 1 for gem_type in gem_types):
        return False
    return (player_action.purchased_card_id is None and
            player_action.reserved_card_id is None and
            player_action.topdeck_level is None)


def is_double_taking_gems(player_action):
    gems_taken = player_action.gems_taken
    gem_types = gem_utils.GetNonEmptyGemTypes(gems_taken)
    if len(gem_types) != 1:
        return False
    gem_type = gem_types[0]
    if gem_type == GemType.GOLD:
        return False
    return (player_action.gems_taken[gem_types[0]] == 2 and
            player_action.purchased_card_id is None and
            player_action.reserved_card_id is None and
            player_action.topdeck_level is None)


def check_player_action(player_game_state, player_action):
    # Cannot take and return same gem.
    gems_taken = player_action.gems_taken
    gems_returned = player_action.gems_returned
    for gem_type in gems_taken:
        if gems_taken[gem_type] > 0 and gems_returned[gem_type] > 0:
            raise ValueError("Cannot take and return the same gem")

    # Gems taken must be avaliable.
    if not gem_utils.VerifyNonNegativeGems(gems_taken):
        raise ValueError("Gem counts must be non-negative")
    gems_available = player_game_state.gem_counts
    if not gem_utils.CanTakeFrom(gems_available, gems_taken):
        raise ValueError("Not enough gems left")

    # Must have enough gems to return.
    self_gems = player_game_state.self_state.gem_counts
    if not gem_utils.VerifyNonNegativeGems(gems_returned):
        raise ValueError("Gem counts must be non-negative")
    if not gem_utils.CanTakeFrom(self_gems, gems_returned):
        raise ValueError("Not enough gems of type " + str(gem_type) + " to return")

    # Must not exceed gem limit.
    num_gems_taken = gem_utils.NumGems(gems_taken)
    excess_gems = num_gems_taken - player_game_state.GemLimit()
    num_gems_returned = gem_utils.NumGems(gems_returned)
    if excess_gems - num_gems_returned > 0:
        raise ValueError("Need to return more gems")

    if is_reserved_revealed_card(player_action):
        # Must not exceed reserve limit.
        if not player_game_state.CanReserve():
            raise ValueError("Can't reserve any more cards")
        # Reserved card must exist.
        card = player_game_state.GetRevealedCardById(
            player_action.reserved_card_id)
        if card is None:
            raise ValueError("Card with asset_id=" + player_action.reserved_card_id
                             + " does not exist")
    elif is_reserved_top_deck(player_action):
        # Must not exceed reserve limit.
        if not player_game_state.CanReserve():
            raise ValueError("Can't reserve any more cards")
        # Reserved card must exist.
        if not player_game_state.CanTopDeck(player_action.topdeck_level):
            raise ValueError("No more cards in deck " + str(player_action.topdeck_level))
    elif is_purchased_card(player_action):
        # Card must exist.
        card = player_game_state.GetReservedOrRevealedCardById(
            player_action.purchased_card_id)
        if card is None:
            raise ValueError("Card with asset_id=" + player_action.reserved_card_id
                             + " does not exist")
        discounted_cost = gem_utils.GetDiscountedCost(
            card.cost, player_game_state.self_state.gem_discounts)
        if not gem_utils.ExactlyPaysFor(discounted_cost,
                                        player_action.gems_returned):
            raise ValueError("Did not exactly pay for card.")
    elif is_taking_different_gems(player_action):
        pass
    elif is_double_taking_gems(player_action):
        gem_types = gem_utils.GetNonEmptyGemTypes(gems_taken)
        if len(gem_types) != 1 or player_game_state.CanTakeTwo(gem_types[0]):
            raise ValueError("Not enough " + str(gem_type) + " gems to take two")
    else:
        raise ValueError("PlayerAction malformed:\n" + str(player_action))

    # Obtaining a noble
    if player_action.noble_tile_id is not None:
        noble_tile = player_game_state.GetNobleById(player_action.noble_tile_id)
        if noble_tile is None:
            raise ValueError("Noble with asset_id=" + player_action.noble_tile_id
                             + " does not exist")
        recently_purchased_gem_type = None
        if player_action.purchased_card_id is not None:
            card = player_game_state.GetReservedOrRevealedCardById(
                player_action.purchased_card_id)
            if card is not None:
                recently_purchased_gem_type = card.gem
        discounts_required = player_action.noble_tile.gem_type_requirements
        discounts_acquired = player_game_state.self_state.gem_discounts
        for gem_type in discounts_required:
            discount_acquired = discounts_acquired[gem_type]
            if gem_type == recently_purchased_gem_type:
                discount_acquired += 1
            if discounts_required[gem_type] > discount_acquired:
                raise ValueError("Don't have the cards to obtain noble tile")
    return

def update_game_state(game_state, player_action, cards_per_level):
    new_game_state = copy.deepcopy(game_state)
    player_id = new_game_state.turn % len(new_game_state.player_states)
    player_state = new_game_state.player_states[player_id]
    
    for gem_type in player_action.gems_taken:
        player_state.gems[gem_type] += player_action.gems_taken[gem_type]
        new_game_state.available_gems[gem_type] -= player_action.gems_taken[gem_type]

    for gem_type in player_action.gems_returned:
        player_state.gems[gem_type] -= player_action.gems_returned[gem_type]
        new_game_state.available_gems[gem_type] += player_action.gems_returned[gem_type]

    if player_action.noble_tile_id is not None:
        for noble in new_game_state.noble_tiles:
            if noble.asset_id == player_action.noble_tile_id:
                new_game_state.noble_tiles.remove(noble)
                player_state.noble_tiles.append(noble)
                break

    action = None
    asset_id = None
    if player_action.reserved_card_id is not None:
        action = "reserve"
        asset_id = player_action.reserved_card_id
    elif player_action.purchased_card_id is not None:
        action = "purchase"
        asset_id = player_action.purchased_card_id

    if action is not None:
        found = False
        for deck in new_game_state.development_cards:
            if found:
                break
            for card in new_game_state.development_cards[deck][-cards_per_level:]:
                if card.asset_id == asset_id:
                    found = True
                    new_game_state.development_cards[deck].remove(card)
                    if action == "reserve":
                        player_state.unhidden_reserved_cards.append(card)
                    if action == "purchase":
                        player_state.purchased_cards.append(card)
                    break
        if not found:
            for card in player_state.unhidden_reserved_cards:
                if card.asset_id == asset_id:
                    found = True
                    player_state.unhidden_reserved_cards.remove(card)
                    player_state.purchased_cards.append(card)
            if not found:
                for card in player_state.hidden_reserved_cards:
                    if card.asset_id == asset_id:
                        player_state.hidden_reserved_cards.remove(card)
                        player_state.purchased_cards.append(card)
    
    if player_action.topdeck_level is not None:
        card = new_game_state.development_cards[player_action.topdeck_level].pop(-cards_per_level-1)
        player_state.hidden_reserved_cards.append(card)

    return new_game_state

