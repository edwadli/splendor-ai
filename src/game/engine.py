"""Utils for running the game."""

# I assume gems taken and returned are nonnegative integers
def check_player_action(player_game_state, player_action):
    self_state = player_game_state.self_state
    is_reserve = player_action.gems_taken[GemType.GOLD]
    gems_taken = gem_utils.CountGems(player_action.gems_taken)
    total_gems_taken = sum(gems_taken)
    num_types_taken = sum([x != 0 for x in gems_taken])
    gems_returned = gem_utils.CountGems(player_action.gems_returned)
    total_gems_returned = sum(gems_returned)
    gem_discounts = self_state.gem_discounts
    
    # Gems taken must be avaliable
    for i in xrange(1, 7):
        if gems_taken[i] > player_game_state.gem_counts[i]:
            return False

    # Must have enough gems to return
    for i in xrange(1, 7):
        if gems_returned[i] > self_state.gem_counts[i] + gems_taken[i]:
            return False

    # Must not exceed gem limit
    if total_gems_taken - total_gems_returned > player_game_state.GemLimit():
        return False

    # Reserving a card
    if is_reserve:
        # Can only take exactly one gold gem
        if is_reserve != 1 or total_gems_taken != 1:
            return False
        # Must not exceed reserve limit
        if not player_game_state.CanReserve():
            return False
        # Must reserve exactly one card
        if player_action.reserved_card_id:
            deck = player_action.reserved_card_id / 100
            if not player_action.reserved_card_id in [x.asset_id for x in player_game_state.revealed_cards[deck]]:
                return False
            if player_action.topdeck_level:
                return False
        elif not player_action.topdeck_level:
            return False
        elif not player_game_state.CanTopDeck(player_action.topdeck_level):
            return False

        # Must not buy a card
        if player_action.purchased_card_id:
            return False
    elif player_action.reserve_card_id or player_action.topdeck_level:
        return False

    # Taking normal gems
    if total_gems_taken and not is_reserve:
        if total_gems_taken > 3:
            return False
        if gems_taken != types_taken:
            if gems_taken != 2:
                return False
            for i in xrange(2, 7):
                if player_action.gems_taken[i]:
                    if not player_game_state.CanTakeTwo(i)
                        return False

    # Buying a card
    if player_action.purchased_card_id:
        # Must not take gems
        if total_gems_taken:
            return False
        deck = player_action.purchased_card_id / 100
        found = False
        for card in player_game_state.revealed_cards[deck] + self_state.reserved_cards:
            if card.asset_id == player_action.purchased_card_id:
                found = True
                costs = gem_utils.CountGems(card.costs)
                gold_needed = 0
                for i in xrange(2, 7):
                    gold_needed += max(0, costs[i] - gem_discounts[i] - gems_returned[i])
                if gold_needed > gems_returned[GemType.GOLD]:
                    return False
                gem_discounts[card.gem] += 1
        if not found:
            return False

    # Obtaining a noble
    if player_action.noble_tile:
        costs = gem_utils.CountGems(player_action.noble_tile.gem_type_requirements)
        for i in xrange(2, 7):
            if costs[i] > gem_discounts[i]:
                return False

    return True




            
