import random

class Game:
    def __init__(self, field_size_x, field_size_y, spike_percentage, coins_per_shield):
        # 0 = empty space
        # 1 = spike
        # 2 = coin
        # 3 = hammer
        self.spike_percentage = spike_percentage
        self.coins_per_shield = coins_per_shield
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.active = False
    
    def getTilesOfType(self,tile_type):
        coordinates = []
        for y in range(self.field_size_y):
            for x in range(self.field_size_x):
                if self.game_map[x][y] == tile_type:
                    coordinates.append((x,y))
        return coordinates            
        
    def start(self):
        self.game_map = [ [0 for y in range(self.field_size_y)] for x in range(self.field_size_x) ] 
        self.score = 0
        self.shields = 0
        self.populateMap()
        coordinates = self.getTilesOfType(0)
        spawn = random.choice(coordinates)
        self.player_x, self.player_y = map(int, spawn)
        self.active = True
    
    def populateMap(self):
        coordinates = self.getTilesOfType(0)
        num_spikes_to_add = int(len(coordinates) * self.spike_percentage)
        selected_tiles = random.sample(coordinates, num_spikes_to_add + 2)
        for i in selected_tiles[:-2]:
            self.game_map[i[0]][i[1]] = 1
        if self.score % self.coins_per_shield == 0 and self.score != 0:
            tile = selected_tiles[-1]
            self.game_map[tile[0]][tile[1]] = 3
        tile = selected_tiles[-2]
        self.game_map[tile[0]][tile[1]] = 2
    
    def move(self, x, y):
        self.player_x += x
        self.player_y += y

        if self.player_x < 0: self.player_x = 0
        if self.player_x >= self.field_size_x: self.player_x = self.field_size_x - 1
        if self.player_y < 0: self.player_y = 0
        if self.player_y >= self.field_size_y: self.player_y = self.field_size_y - 1

        #check if the player collected a coin
        if self.game_map[self.player_x][self.player_y] == 2:
            self.score += 1
            self.populateMap()
            self.game_map[self.player_x][self.player_y] = 0

        #check if the player collected a shield
        if self.game_map[self.player_x][self.player_y] == 3:
            self.shields += 1
            self.game_map[self.player_x][self.player_y] = 0

        #check if the player hit a spike
        if self.game_map[self.player_x][self.player_y] == 1:
            if self.shields > 0:
                self.shields -= 1
                self.game_map[self.player_x][self.player_y] = 0
            else:
                self.active = False
        