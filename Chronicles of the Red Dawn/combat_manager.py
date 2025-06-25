import random
class Combat_Manager():
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.current_turn = random.choice([self.player, self.enemies])  # First action is randomized
        self.action_cooldown = 100 # Frame time before an action can be taken
        self.action_wait = 0 # Counter for action cooldown

    def update_player_phase(self):
        """Update the player's phase of combat."""
        # Resets player's base defense at the start of their turn
        if self.action_wait == 0 and self.player.defense != self.player.base_defense:
            self.player.defense = self.player.base_defense

        self.action_wait += 1
    
    def player_action_ready(self):
        """Check if the player can take an action."""
        return self.action_wait >= self.action_cooldown

    def player_attack(self):
        """Handle the player's attack action."""
        if self.player_action_ready():
            damage = self.player.attack(self.enemies)
            self._end_turn()
            return damage # Returns damage dealt
        return None # Action not ready
    
    def player_guard(self):
        """Handle the player's guard action."""
        # Increases player's defense for the turn
        if self.player_action_ready():
            self.player.guard() # Increase defense by 50%
            self._end_turn()
            return True # Action was successful
        return None # Action not ready
    
    def player_heal(self, amount):
        """Handle the player's heal action."""
        if self.player_action_ready():
            heal_amount = self.player.heal(amount)
            self._end_turn()
            return heal_amount
        return None
    
    def player_pass(self):
        """Handle the player's pass action."""
        # Player can pass their turn without taking an action
        if self.player_action_ready():
            self._end_turn()
            return True # Action was successful
        return False # Action not ready
    
    def update_enemy_phase(self):
        """Update the enemy's phase of combat."""
        self.action_wait += 1
        if self.action_wait >= self.action_cooldown:
            if self.enemies.is_alive:
                damage = self.enemies.attack(self.player)
                self._end_turn()
                return damage # Returns damage dealt
            self._end_turn()
            return None
        return None # Enemies not ready to attack

    def _end_turn(self):
        """Switcthes the turn to the other combatant."""
        if self.current_turn == self.player:
            self.current_turn = self.enemies
        else:
            self.current_turn = self.player
        self.action_wait = 0 # Reset action wait for the next turn
    
    def is_player_turn(self):
        """Check if it's the player's turn."""
        return self.current_turn == self.player
    
    def is_enemy_turn(self):
        """Check if it's the enemy's turn."""
        return self.current_turn == self.enemies