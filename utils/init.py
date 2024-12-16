import pygame
import utils.Colors as Colors

# Some initialization before the game starts
def initialize():
  Trollicon=pygame.image.load('images/Trollman.png')
  pygame.display.set_icon(Trollicon)

  #Add music
  pygame.mixer.init()
  pygame.mixer.music.load('pacman.mp3')
  pygame.mixer.music.play(-1, 0.0)


  # Call this function so the Pygame library can initialize itself
  pygame.init()
    
  # Create an 606x606 sized screen
  screen = pygame.display.set_mode([606, 606])

  # This is a list of 'sprites.' Each block in the program is
  # added to this list. The list is managed by a class called 'RenderPlain.'


  # Set the title of the window
  pygame.display.set_caption('Pacman')

  # Create a surface we can draw on
  background = pygame.Surface(screen.get_size())

  # Used for converting color maps and such
  background = background.convert()
    
  # Fill the screen with a black background
  background.fill(Colors.black)



  clock = pygame.time.Clock()

  pygame.font.init()
  font = pygame.font.Font("freesansbold.ttf", 24)

  #default locations for Pacman and monstas
  w = 303-16 #Width
  p_h = (7*60)+19 #Pacman height
  m_h = (4*60)+19 #Monster height
  b_h = (3*60)+19 #Binky height
  i_w = 303-16-32 #Inky width
  c_w = 303+(32-16) #Clyde width
  
  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0

  state = {
    "w": w,
    "p_h": p_h,
    "m_h": m_h,
    "b_h": b_h,
    "i_w": i_w,
    "c_w": c_w,
    "screen": screen,
    "clock": clock,
    "font": font,
    "p_turn": p_turn,
    "p_steps": p_steps,
    "b_turn": b_turn,
    "b_steps": b_steps,
    "i_turn": i_turn,
    "i_steps": i_steps,
    "c_turn": c_turn,
    "c_steps": c_steps
  }

  return state