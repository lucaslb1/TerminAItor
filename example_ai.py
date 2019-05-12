from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS, BLD_HOME
from AI import AI
game = Colorfight()

game.connect(room = 'public')

if game.register(username = 'LAX_AI', password = "potter"):
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

        #turn_analysis = AI(game)
        # Upgrade home
        for cell in game.me.cells.values():

            if cell.building.is_home and cell.building.level == 1 and me.gold > 1000 and me.energy > 1000:
                cmd_list.append(game.upgrade(cell.position))
                #print("We upgrade {} on ({}, {})".format("HOME", cell.position.x, cell.position.y))
                me.gold -= 1000
                me.energy -= 1000
                break;

            elif cell.building.is_home and cell.building.level == 2 and me.gold > 2000 and me.energy > 2000:
                cmd_list.append(game.upgrade(cell.position))
                #print("We upgrade {} on ({}, {})".format("HOME", cell.position.x, cell.position.y))
                me.gold -= 2000
                me.energy -= 2000
                break;

        # find the best cells to attack
        best_cells = []
        for cell in game.me.cells.values():

            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Finds valid cells
                c = game.game_map[pos]

                if c.owner != game.uid and c.attack_cost < me.energy:
                    a_cell_pair = (c.position, c.natural_energy/c.attack_cost)
                    if a_cell_pair not in best_cells:
                        best_cells.append(a_cell_pair)

        # Attack new cells
        best_cells.sort(key=lambda X: X[1], reverse=True)

        for pair in best_cells:
            c = game.game_map[pair[0]]

            if c.position not in my_attack_list:
                cmd_list.append(game.attack(pair[0], c.attack_cost))
                #print("We are attacking ({}, {}) Value({})".format(pair[0].x, pair[0].y, pair[1]), end ='')
                game.me.energy -= c.attack_cost
                my_attack_list.append(c.position)
        #print("")


        # Build buildings
        best_build_cells = sorted(game.me.cells.values(), key=lambda X: X.natural_energy + X.natural_gold, reverse=True)
        for cell in best_build_cells:
            if me.gold > 100 and cell.building.is_empty:
                if me.gold>200 or game.turn>100:
                    is_adjacent = False
                    for adj in cell.position.get_surrounding_cardinals():
                        if not game.game_map[adj].is_empty and game.game_map[adj].owner != game.uid:
                            is_adjacent = True
                            print(is_adjacent)

                    if is_adjacent:
                        cmd_list.append(game.build(cell.position, BLD_FORTRESS))
                        me.gold-=100

                elif cell.natural_gold < (cell.natural_energy+1):
                    cmd_list.append(game.build(cell.position, BLD_ENERGY_WELL))
                    # print("We build {} on ({}, {})".format("ENERGY WELL", cell.position.x, cell.position.y), end='')
                    me.gold -= 100

                else:
                    cmd_list.append(game.build(cell.position, BLD_GOLD_MINE))
                    # print("We build {} on ({}, {})".format("GOLD MINE", cell.position.x, cell.position.y), end='')
                    me.gold -= 100
        #print("")


        #Upgrade buildings
        lvl_one_buildings = []
        lvl_two_buildings = []
        for cell in game.me.cells.values():
            if cell.building is not None and cell.building != "home" and cell.building.level == 1:
                lvl_one_buildings.append(cell)
            elif cell.building is not None and cell.building != "home" and cell.building.level == 2:
                lvl_two_buildings.append(cell)

        best_lvl_one_buildings = sorted(lvl_one_buildings, key=lambda X: X.natural_energy+X.natural_gold, reverse=True)
        best_lvl_two_buildings = sorted(lvl_two_buildings, key=lambda X: X.natural_energy+X.natural_gold, reverse=True)
        if me.tech_level > 1:
            for cell in best_lvl_one_buildings:
                if me.gold > 200:
                    cmd_list.append(game.upgrade(cell.position))
                    #print("We upgrade {} on ({}, {})".format(cell.building, cell.position.x, cell.position.y),end='')
                    me.gold -= 200
            #print("")
        if me.tech_level > 2:
            for cell in best_lvl_two_buildings:
                if me.gold > 300:
                    cmd_list.append(game.upgrade(cell.position))
                    #print("We upgrade {} on ({}, {})".format(cell.building, cell.position.x, cell.position.y),end='')
                    me.gold -= 300
            #print("")

        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        #print(result)
