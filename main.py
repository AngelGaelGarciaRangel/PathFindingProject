#Import the necessary libraries
from tkinter import messagebox, Tk 
import pygame
import sys
#Create the  window
wwidth = 500
wheight = 500
window = pygame.display.set_mode((wwidth, wheight))
#Create all the necessary for the grid
col = 25
row = 25
bwidth = wwidth // col
bheight = wheight // row
grid = []
#Create the class that will be helping to make the grid
class Box:
  def __init__(self, i, j):
    self.x = i
    self.y = j
    #Flags to make a difference with start, end and obstacles
    self.start = False
    self.end = False
    self.obstacle = False
  def draw(self, w, color):
    pygame.draw.rect(w, color, (self.x *bwidth, self.y * bheight, bwidth - 2, bheight - 2))
#Create the grid by iterate over all the possible positions
for i in range(col):
  array = []
  for j in range(row):
    array.append(Box(i, j))
  grid.append(array)
start_box = grid[0][0]
start_box.start = True
#Specify the main function
def main():
  begin_search = False
  end_box_set = False
  end_box  = None
  while True:
    for event in pygame.event.get():
      #If user wants to exit
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit
      #Mouse controls for the wall
      elif event.type == pygame.MOUSEMOTION:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        # Draw the wall
        if pygame.mouse.get_pressed()[0]:
          i = x // bwidth
          j = y // bheight
          grid[i][j].obstacle = True
        #Draw the end of the path
        if event.buttons[2] and not end_box_set:
          i = x // bwidth
          j = y // bheight
          end_box = grid[i][j]
          end_box.end = True
          end_box_set = True
      #If user put the end of the path, start the algorithm
      if event.type == pygame.KEYDOWN and end_box_set:
        begin_search = True
   #Specify the color of the box
    window.fill((0, 0, 0))
   #Draw the grid 
    for i in range(col):
      for j in range(row):
        box = grid[i][j]
        box.draw(window, (50, 50, 50))
        if box.start:
          box.draw(window, (0, 200, 200))
        if box.end:
          box.draw(window, (200, 200, 0))
        if box.obstacle:
          box.draw(window, (90, 90, 90))
   #Update the display
    pygame.display.flip()
main()
