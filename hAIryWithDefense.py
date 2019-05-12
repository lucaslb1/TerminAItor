from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS, BLD_HOME

game = Colorfight()

game.connect(room = 'public')

mode = 'expansion'

def formation():
    if mode == 'defense' and cell.owner == me.uid and cell.building.is_empty and me.gold >= 100:
        building = random.choice([BLD_FORTRESS, BLD_FORTRESS, BLD_FORTRESS, BLD_FORTRESS, BLD_GOLD_MINE, BLD_ENERGY_WELL])
        cmd_list.append(game.build(cell.position, building))
        print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
        me.gold -= 100

if game.register(username = 'hAIryP0tter', password = "potter"):
    # This is the game loop

    while True:
        # The command list we will send to the server
        cmd_list = []
        # The list of cells that we want to attack
        my_attack_list = []
        # update_turn() is required to get the latest information from the
        # server. This will halt the program until it receives the updated
        # information.
        # After update_turn(), game object will be updated.
        game.update_turn()

        # Check if you exist in the game. If not, wait for the next round.
        # You may not appear immediately after you join. But you should be
        # in the game after one round.
        if game.me == None:
            continue

        me = game.me

        # find the best cells to attack
        best_cells = []
        for cell in game.me.cells.values():
            if cell.building.is_home and cell.building.level == 1 and me.gold > 1000 and me.energy > 1000:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgrade {} on ({}, {})".format("HOME", cell.position.x, cell.position.y))
                me.gold -= 1000
                me.energy -= 1000

            elif cell.building.is_home and cell.building.level == 2 and me.gold > 2000 and me.energy > 2000:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgrade {} on ({}, {})".format("HOME", cell.position.x, cell.position.y))
                me.gold -= 2000
                me.energy -= 2000

            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Finds valid cells
                c = game.game_map[pos]

                # If there are nearby AI, sets mode to defense.
                if cell.owner != me.uid and cell.owner != game.uid:
                    mode = 'defense'

                formation()

                if c.owner != game.uid and c.attack_cost < me.energy:
                    a_cell_pair = (c.position, c.natural_energy/c.attack_cost)
                    if a_cell_pair not in best_cells:
                        best_cells.append(a_cell_pair)

        best_cells.sort(key=lambda X: X[1], reverse=True)
        for pair in best_cells:
            c = game.game_map[pair[0]]

            # Add the attack command in the command list
            # Subtract the attack cost manually so I can keep track
            # of the energy I have.
            # Add the position to the attack list so I won't attack
            # the same cell
            if c.position not in my_attack_list:
                cmd_list.append(game.attack(pair[0], c.attack_cost))
                print("We are attacking ({}, {}) Value({})".format(pair[0].x, pair[0].y, pair[1]), end ='')
                game.me.energy -= c.attack_cost
                my_attack_list.append(c.position)
        print("")
        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.

        lvl_one_buildings = []
        lvl_two_buildings = []
        for cell in game.me.cells.values():
            if cell.building is not None and cell.building != "home" and cell.building.level == 1:
                lvl_one_buildings.append(cell)
            elif cell.building is not None and cell.building != "home" and cell.building.level == 2:
                lvl_two_buildings.append(cell)

        best_lvl_one_buildings = sorted(lvl_one_buildings, key=lambda X: X.natural_energy+X.natural_gold, reverse=True)
        best_lvl_two_buildings = sorted(lvl_two_buildings, key=lambda X: X.natural_energy+X.natural_gold, reverse=True)

        for cell in best_lvl_one_buildings:
            if me.gold > 200:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgrade {} on ({}, {})".format(cell.building, cell.position.x, cell.position.y),end='')
                me.gold -= 200
        print("")

        for cell in best_lvl_two_buildings:
            if me.gold > 300:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgrade {} on ({}, {})".format(cell.building, cell.position.x, cell.position.y),end='')
                me.gold -= 300
        print("")

        best_build_cells = sorted(game.me.cells.values(), key=lambda X: X.natural_energy + X.natural_gold, reverse=True)

        for cell in best_build_cells:
            if me.gold > 100 and cell.building.is_empty:
                if cell.natural_gold > (cell.natural_energy + 1):
                    cmd_list.append(game.build(cell.position, BLD_GOLD_MINE))
                    print("We build {} on ({}, {})".format("GOLD MINE", cell.position.x, cell.position.y), end='')
                    me.gold -= 100
                else:
                    cmd_list.append(game.build(cell.position, BLD_ENERGY_WELL))
                    print("We build {} on ({}, {})".format("ENERGY WELL", cell.position.x, cell.position.y), end='')
                    me.gold -= 100
        print("")
        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)