from .Character import Character

# This class represents the bar at the bottom that the player controls
class Player(Character):
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y