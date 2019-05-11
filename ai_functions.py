

# Returns the gold gained after the game ends by upgrading a cell
def eval_mine_upgrade(game, cell):
    if cell.owner == game.me:
        current_level = cell.building.level

        # check if you get gold on the turn you build something
        pre_total_gold = cell.gold * (500 - game.turn) #check if you get gold on the turn you build something
        post_total_gold = cell.natural_gold * (current_level+2)*(500-game.turn) - cell.building.upgrade_gold
        gold_difference = post_total_gold - pre_total_gold
        return gold_difference
    else:
        return None


# Returns the energy gained after the game ends by upgrading a cell
def eval_well_upgrade(game, cell):
    if cell.owner == game.me:
        current_level = cell.building.level

        # check if you get gold on the turn you build something
        pre_total_energy = cell.gold * (500 - game.turn) #check if you get gold on the turn you build something
        post_total_energy = cell.natural_gold * (current_level+2)*(500-game.turn)
        energy_difference = post_total_energy - pre_total_energy
        return energy_difference
    else:
        return None


# Returns cell evaluation based on energy gained for empty cells
def empty_cell_energy_gained(game, cell):
    if cell.owner == 0:
        return cell.natural_energy * (500-game.turn) - cell.natural_cost
    else:
        return None


# Returns gold gained after game ends empty cell
def empty_cell_gold_gained(game, cell):
    if cell.owner == 0:
        return cell.natural_gold * (500 - game.turn)
    else:
        return None


# Returns ratio of energy
def empty_cell_value(game, cell):
    if cell.owner == 0:
        total_energy = empty_cell_energy_gained(game, cell)
        total_gold = empty_cell_gold_gained(game, cell)
        return total_energy + total_gold

    else:
        return None
