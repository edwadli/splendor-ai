"""Utils for running the game."""

from src.proto.gem_proto import GemType

# I assume gems taken and returned are nonnegative integers
def check_player_action(player_game_state, player_action):
    self_state = player_game_state.self_state
    gems_taken = player_action.gems_taken
    total_gems_taken = sum(gems_taken.values())
    is_reserve = GemType.GOLD in gems_taken
    num_types_taken = sum([x != 0 for x in gems_taken])
    gems_returned = player_action.gems_returned
    total_gems_returned = sum(gems_returned)
    gem_discounts = self_state.gem_discounts
    
    # Gems taken must be avaliable
    for gem_type in gems_taken:
        if gems_taken[gem_type] > player_game_state.gem_counts[gem_type]:
            raise ValueError("Not enough gems left of type " + str(gem_type))

    # Must have enough gems to return
    for gem_type in gems_returned:
        if gems_returned[i] > self_state.gem_counts[i]:
            raise ValueError("Not enough gems of type " + str(gem_type) + " to return")

    # Must not exceed gem limit
    if total_gems_taken - total_gems_returned > player_game_state.GemLimit():
        raise ValueError("Exceeded total gem limit")

    # Reserving a card
    if is_reserve:
        # Can only take exactly one gold gem
        if total_gems_taken != 1:
            raise ValueError("Took " + str(total_gems_taken) + " gems while reserving")
        # Must not exceed reserve limit
        if not player_game_state.CanReserve():
            raise ValueError("Can't reserve any more cards")
        # Must reserve exactly one card
        if player_action.reserved_card_id:
            player_game_state.GetReservedCardById(player_action.reserved_card_id)
            if player_action.topdeck_level:
                raise ValueError("Can't reserved a revealed card and topdeck")
        elif not player_action.topdeck_level:
            raise ValueError("Did not specify which card to reserve")
        elif not player_game_state.CanTopDeck(player_action.topdeck_level):
            raise ValueError("No more cards in deck " + str(player_action.topdeck_level))

        # Must not buy a card
        if player_action.purchased_card_id:
            raise ValueError("Can't reserve and buy in the same action")
    elif player_action.reserved_card_id or player_action.topdeck_level:
        raise ValueError("Not reserving but specified a card to be reserved")

    # Taking normal gems
    if total_gems_taken and not is_reserve:
        if total_gems_taken > 3:
            raise ValueError("Too many gems taken: " + str(total_gems_taken))
        if total_gems_taken != num_types_taken:
            if total_gems_taken != 2:
                raise ValueError("Can only take two gems of same color")
            for gem_type in gems_taken:
                if not player_game_state.CanTakeTwo(gem_type):
                    raise ValueError("Not enough " + str(gem_type) + " gems to take two")

    # Buying a card
    if player_action.purchased_card_id:
        # Must not take gems
        if total_gems_taken:
            raise ValueError("Can't buy and take gems")
        card = GetRevealedCardById(player_action.purchased_card_id)
        if not card:
            card = GetReservedCardById(player_action.purchased_card_id)
        if not card:
            raise ValueError("Card with asset_id=" + str(player_action.purchased_card_id) + " not found")
        costs = card.costs
        gold_needed = 0
        for gem_type in costs:
            gold_needed += max(0, costs[gem_type] - gem_discounts[gem_type] - gems_returned[gem_type])
        if gold_needed > gems_returned[GemType.GOLD]:
            return ValueError("Card costs too much")
        gem_discounts[card.gem] += 1

    # Obtaining a noble
    if player_action.noble_tile_id:
        noble_tile = player_game_state.GetNobleById(player_action.noble_tile_id)
        costs = player_action.noble_tile.gem_type_requirements
        for gem_type in costs:
            if costs[gem_type] > gem_discounts[gem_type]:
                raise ValueError("Don't have the cards to obtain noble tile")

    return True




            
