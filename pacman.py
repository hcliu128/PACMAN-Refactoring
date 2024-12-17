#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
import pygame

from character.Player import Player
from character.Ghost import Ghost
from utils.Block import Block
from utils.Settings import Blinky_directions, Inky_directions, Clyde_directions, Pinky_directions, pl, bl, il, cl
import utils.Wall as Wall
import utils.Colors as Colors
from utils.init import initialize

def startGame():
  global screen, font, clock
  GameState = initialize()
  screen, w, p_h, m_h, b_h, i_w, c_w, clock, font = GameState["screen"], GameState["w"], GameState["p_h"], GameState["m_h"], GameState["b_h"], GameState["i_w"], GameState["c_w"], GameState["clock"], GameState["font"]
  p_turn, p_steps, b_turn, b_steps, c_turn, c_steps, i_turn, i_steps = GameState["p_turn"], GameState["p_steps"], GameState["b_turn"], GameState["b_steps"], GameState["c_turn"], GameState["c_steps"], GameState["i_turn"], GameState["i_steps"] 

  all_sprites_list = pygame.sprite.RenderPlain()
  block_list = pygame.sprite.RenderPlain()
  monsta_list = pygame.sprite.RenderPlain()
  pacman_collide = pygame.sprite.RenderPlain()
  wall_list = Wall.setupRoomOne(all_sprites_list)
  gate = Wall.setupGate(all_sprites_list)

  # Create the player paddle object
  Pacman = Player( w, p_h, "images/Trollman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky=Ghost( w, b_h, "images/Blinky.png", "Blinky" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "images/Pinky.png", "Pinky" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "images/Inky.png", "Inky" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "images/Clyde.png", "Clyde" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(Colors.yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)
  score = 0
  done = False
  characters = [Pinky, Blinky, Inky, Clyde]
  turn_steps = {"Pinky": [p_turn, p_steps], "Blinky": [b_turn, b_steps], "Inky": [i_turn, i_steps], "Clyde": [c_turn, c_steps]}
  directions = [Pinky_directions, Blinky_directions, Inky_directions, Clyde_directions]
  lengths = [pl, bl, il, cl]
  while not done:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30, 0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30, 0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0, -30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0, 30)

          # 避免鬆開按鈕還在移動
          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)

      
      for idx, character in enumerate(characters):
        ret = character.changespeed(directions[idx], character.name, turn_steps[character.name][0], turn_steps[character.name][1], lengths[idx])
        turn_steps[character.name][0] = ret[0]
        turn_steps[character.name][1] = ret[1]
        character.changespeed(directions[idx], character.name, turn_steps[character.name][0], turn_steps[character.name][1], lengths[idx])
        character.update(wall_list,False)

      # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True) # True -> delete the blocks and return a list of blocks
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score += len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(Colors.black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, Colors.red)
      screen.blit(text, [10, 10])

      if score == bll:
        doNext("Congratulations, you won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate)
      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
      if monsta_hit_list:
        doNext("Game Over", 235, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1 = font.render(message, True, Colors.white)
      screen.blit(text1, [left, 233])

      text2 = font.render("To play again, press ENTER.", True, Colors.white)
      screen.blit(text2, [135, 303])
      text3 = font.render("To quit, press ESCAPE.", True, Colors.white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)


if __name__ == "__main__":
  startGame()
  pygame.quit()