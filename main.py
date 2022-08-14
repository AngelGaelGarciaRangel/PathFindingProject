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
#queue that will have the nodes
queue = []
#array that will have the pat
path = []
#Create the class that will be helping to make the grid
class Box:
  def __init__(self, i, j):
    self.x = i
    self.y = j
    #Flags to make a difference with start, end and obstacles
    self.start = False
    self.end = False
    self.obstacle = False
    #if the box is already on the queue or not
    self.queue = False
    #if the box have been visited
    self.visited = False
    #neighbours of each box
    self.neighbours = []
    self.prior = None
  def draw(self, w, color):
    pygame.draw.rect(w, color, (self.x *bwidth, self.y * bheight, bwidth - 2, bheight - 2))
  def set_neighbours(self):
    #if the box have an horizontal left neighbour, add it
    if self.x > 0:
      self.neighbours.append(grid[self.x - 1][self.y])
    #if the box have an horizontal right neighbour, add it
    if self.x < col - 1:
      self.neighbours.append(grid[self.x + 1][self.y])
    #if the box have a vertical up neighbour, add it
    if self.y > 0:
      self.neighbours.append(grid[self.x][self.y - 1])
    #if the box have a vertical down neighbour, add it  
    if self.y < row - 1:
      self.neighbours.append(grid[self.x][self.y + 1])
#Create the grid by iterate over all the possible positions
for i in range(col):
  array = []
  for j in range(row):
    array.append(Box(i, j))
  grid.append(array)
#Set the neighbours for all the boxes
for i in range(col):
  for j in range(row):
    grid[i][j].set_neighbours()

#start_box = grid[0][0]
#start_box.start = True
#put the start_box into the queue
#queue.append(start_box)
#start_box.visited = True
#Specify the main function
def main():
  begin_search = False
  end_box_set = False
  end_box  = None
  searching = True
  start_box_set = False
  while True:
    for event in pygame.event.get():
      #If user wants to exit
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit
      #Mouse controls for the wall
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and not start_box_set:
          i = x // bwidth
          j = y // bheight
          start_box = grid[i][j]
          start_box.start = True
          queue.append(start_box)
          start_box.visited = True
          start_box_set = True
        elif event.button == 3 and not end_box_set:
          i = x // bwidth
          j = y // bheight
          end_box = grid[i][j]
          end_box.end = True
          end_box_set = True
          begin_search = True
      elif event.type == pygame.MOUSEMOTION:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        # Draw the wall
        if pygame.mouse.get_pressed()[0] and start_box_set:
          i = x // bwidth
          j = y // bheight
          grid[i][j].obstacle = True
    if begin_search:
      if len(queue) > 0 and searching:
        current_box = queue.pop(0)
        current_box.visited = True
        if current_box == end_box:
          searching = False
          while current_box.prior != start_box:
            path.append(current_box.prior)
            current_box = current_box.prior
        else:
          for neighbour in current_box.neighbours:
            if not neighbour.queue and not neighbour.obstacle:
              neighbour.queue = True
              neighbour.prior = current_box
              queue.append(neighbour)
      #if queue is 0 and we never found the solution
      else:
        if searching:
          Tk().wm_withdraw()
          messagebox.showinfo("No solution", "There is no solution")
          searching = False
   #Specify the color of the box
    window.fill((0, 0, 0))
   #Draw the grid 
    for i in range(col):
      for j in range(row):
        box = grid[i][j]
        box.draw(window, (50, 50, 50))
        if box.queue:
          box.draw(window, (200, 0, 0))
        if box.visited:
          box.draw(window, (0, 200, 0))
        if box in path:
          box.draw(window, (0, 0, 200))
        if box.start:
          box.draw(window, (0, 200, 200))
        if box.end:
          box.draw(window, (200, 200, 0))
        if box.obstacle:
          box.draw(window, (90, 90, 90))
   #Update the display
    pygame.display.flip()
main()

