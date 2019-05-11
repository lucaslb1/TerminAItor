from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

game = Colorfight()

game.connect(room = 'test_room2')

if game.register(username = 'hAiry', password = "potter"):
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

        best_cells = []
        #find the best cells
        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Finds valid cells
                c = game.game_map[pos]

                if c.owner != game.uid and c.attack_cost < me.energy:
                    a_cell_pair = (c.position, c.natural_energy/c.attack_cost)
                    if a_cell_pair not in best_cells:
                        best_cells.append(a_cell_pair)

        best_cells.sort(key=lambda X: X[1], reverse=True)
        print(best_cells)
        for pair in best_cells:
            c = game.game_map[pair[0]]

            # Add the attack command in the command list
            # Subtract the attack cost manually so I can keep track
            # of the energy I have.
            # Add the position to the attack list so I won't attack
            # the same cell
            if c.position not in my_attack_list:
                cmd_list.append(game.attack(pair[0], c.attack_cost))
                print("We are attacking ({}, {}) Value({})".format(pair[0].x, pair[0].y, pair[1]))
                game.me.energy -= c.attack_cost
                my_attack_list.append(c.position)

        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.

        best_build_cells = sorted(game.me.cells.values(), key=lambda X: X.natural_energy+X.natural_gold, reverse=True)

        for cell in best_build_cells:
            if me.gold>100 and cell.building.is_empty:
                if cell.natural_gold>(cell.natural_energy+1):
                    cmd_list.append(game.build(cell.position, BLD_GOLD_MINE))
                    print("We build {} on ({}, {})".format("GOLD MINE", cell.position.x, cell.position.y))
                    me.gold -= 100
                else:
                    cmd_list.append(game.build(cell.position, BLD_ENERGY_WELL))
                    print("We build {} on ({}, {})".format("ENERGY WELL", cell.position.x, cell.position.y))
                    me.gold -= 100

        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
