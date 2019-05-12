class AI:
    def __init__(self, game):

        # All lists
        self.best_attack = []

        self.best_build_mine = []
        self.best_build_well = []
        self.best_build_fortress = []  # to-do

        self.best_upgrade_mine = []
        self.best_upgrade_well = []
        self.best_upgrade_fortress = [] #to-do

        self.upgrade_home = False #to-do

        # Go through all my cells
        for cell in game.me.cells.values():

            #Adds potential buildings to lists
            if cell.building.is_empty and cell not in self.best_build_well and cell not in self.best_build_mine:
                self.best_build_mine.append(cell)
                self.best_build_well.append(cell)

            # Adds potential upgrades to lists
            if not cell.building.is_empty and cell.building.name != "home" and cell.building.level < game.me.tech_level:
                if cell.building.name == "gold_mine" :
                    self.best_upgrade_mine.append(cell)
                elif cell.building.name == "energy_well":
                    self.best_upgrade_mine.append(cell)


            #Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Finds valid cells
                c = game.game_map[pos]

                # Adds fortress list
                if c.owner != game.uid and c.owner != 0 and cell.building.is_empty and cell not in self.best_build_fortress:
                    self.best_build_fortress.append(cell)

                # Add best cells to attack based
                if c.owner != game.uid and c.attack_cost < game.me.energy:
                    if c not in self.best_attack:
                        self.best_attack.append(c)



        # Sort attack list
        self.best_attack.sort(key=lambda X: X.natural_gold + X.natural_energy/X.attack_cost, reverse=True)

        # Sort where to build stuff
        self.best_build_mine.sort(key=lambda X: X.natural_gold, reverse =True)
        self.best_build_well.sort(key=lambda X: X.natural_energy, reverse=True)

        # Sort what I should upgrade, lvl1 buildings upgrade first
        self.best_upgrade_mine.sort(key=lambda X: X.natural_gold - X.building.level * 10 ,reverse=True)
        self.best_upgrade_well.sort(key=lambda X: X.natural_energy - X.building.level * 10, reverse=True)

        print("attacks {}: fortress{}: build_mine{}: build_well{}: upgrade_mine{}: upgrade_well{}".format(len(self.best_attack)\
        , len(self.best_build_fortress), len(self.best_build_mine), len(self.best_build_well), len(self.best_upgrade_mine), len(self.best_upgrade_well)))
