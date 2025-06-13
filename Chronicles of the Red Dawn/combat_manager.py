class Combat_Manager():
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.current_turn = player
        self.turn_active = True
        self.action_cooldown = 100
        self.action_wait = 0

    def player_phase(self):
        if self.current_turn == self.player:
            if self.player.is_alive == True:
                if self.turn_active == True:
                    self.player.defense = 20
                    self.action_wait += 1
    
    def player_attack(self):
        if self.action_wait > self.action_cooldown:
            self.player.attack(self.enemies)
            self.turn_active = False
            self.action_wait = 0
    
    def player_guard(self):
        if self.action_wait > self.action_cooldown:
            self.player.defense *= 0.7
            self.turn_active = False
            self.action_wait = 0
    
    def player_pass(self):
        if self.action_wait > self.action_cooldown:
            self.turn_active = False
            self.action_wait = 0
    
    def enemy_phase(self):
        if self.turn_active == False:
            if self.enemies.is_alive == True:
                if self.turn_active == False:
                    self.action_wait += 1
                    if self.action_wait > self.action_cooldown:
                        self.enemies.attack(self.player)
                        self.turn_active = True
                        self.action_wait = 0

    
    def draw(self):
        self.player_phase()
        self.enemy_ai()