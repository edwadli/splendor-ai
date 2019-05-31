"""Utils for running the game."""

# I assume gems taken and returned are nonnegative integers
def is_valid(gamestate, player_action, player_id, gamerules):
    player = Player(gamestate.player_states[player_id])
    reserve = player_action.gems_taken[GemType.GOLD]
    gems_taken = sum(player_action.gems_taken)
    types_taken = sum([x != 0 for x in player_action.gems_taken])
    gems_returned = sum(player_action.gems_returned)
    
    # Gems taken must be avaliable
    for i in xrange(6):
        if player_action.gems_taken[i] > gamestate.gems[i]:
            return False

    # Must have enough gems to return
    for i in xrange(6):
        if player_action.gems_returned[i] > player.gems[i] + player_action.gems_taken[i]:
            return False

    # Must not exceed gem limit
    if sum(player.gems) + gems_taken - gems_returned > gamerules.max_gems:
        return False

    # Reserving a card
    if reserve:
        # Can only take exactly one gold gem
        if reserve != 1 or gems_taken != 1:
            return False
        # Must not exceed reserve limit
        if player.num_reserved_cards >= gamerules.max_reserved_cards:
            return False
        # Must reserve exactly one card
        if player_action.reserved_card_id:
            level = player_action.reserved_card_id / 100
            if not player_action in [x.asset_id for x in gamestate.cards[level - 1]]:
                return False
            if player_action.topdeck_level:
                return False
        elif not player_action.topdeck_level:
            return False
        # Must not buy a card
        if player_action.purchased_card_id:
            return False
    elif player_action.reserve_card_id or player_action.topdeck_level:
        return False

    # Taking normal gems
    if gems_taken and not reserve:
        # Can take at most 3 gems
        if gems_taken > 3:
            return False
        # Can only take two of one color if there are at least 
        if gems_taken != types_taken:
            if gems_taken != 2:
                return False
            for i in xrange(1, 6):
                if player_action.gems_taken[i]:
                    if gamestate.gems[i] < gamerules.min_double_take_gems:
                        return False

    # Buying a card
    if player_action.purchased_card_id:
        # Must not take gems
        if gems_taken:
            return False
        level = player_action.purchased_card_id / 100
        found = False
        # hidden reserved cards ???
        for card in gamestate.cards[level - 1] + player.reserved_cards:
            if card.asset_id == player_action.purchased_card_id:
                found = True
                gold_needed = 0
                for i in xrange(1, 6):
                    gold_needed += max(0, card.costs[i] - player.discounts[i] - player_action.gems_returned[i])
                if gold_needed > player.action.gems_returned[GemType.GOLD]:
                    return False

        if not found:
            return False

    return True




            
