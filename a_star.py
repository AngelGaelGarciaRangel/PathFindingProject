#Import the necessary libraries
from tkinter import messagebox, Tk 
import pygame
import sys
from queue import PriorityQueue
#Create the  window
wwidth = 1000
wheight = 1000
window = pygame.display.set_mode((wwidth, wheight))
pygame.display.set_caption("Path finding algorithm")
#Create all the necessary for the grid
col = 50
row = 50
bwidth = wwidth // col
bheight = wheight // row
grid = []
#Priority queue that will be having every node
queue = []
#Set that will only have the object
setObjects = []
#Array that will have the path
path = []
#Map with object:prior
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
    self.f_score = float("inf")
    self.g_score = float("inf")
  def draw(self, w, color):
    pygame.draw.rect(w, color, (self.x *bwidth, self.y * bheight, bwidth - 2, bheight - 2))
  def set_neighbours(self):
    #if the box have an horizontal left neighbour, add it
    if self.x > 0 and not grid[self.x - 1][self.y].obstacle:
      self.neighbours.append(grid[self.x - 1][self.y])
    #if the box have an horizontal right neighbour, add it
    if self.x < col - 1 and not grid[self.x + 1][self.y].obstacle:
      self.neighbours.append(grid[self.x + 1][self.y])
    #if the box have a vertical up neighbour, add it
    if self.y > 0 and not grid[self.x][self.y - 1].obstacle:
      self.neighbours.append(grid[self.x][self.y - 1])
    #if the box have a vertical down neighbour, add it  
    if self.y < row - 1 and not grid[self.x][self.y + 1].obstacle:
      self.neighbours.append(grid[self.x][self.y + 1])
#function that calculate the h with respect to two boxes and the specific formula
def calculateH(box1, box2):
  x1 = box1.x
  x2 = box2.x
  y1 = box1.y
  y2 = box2.y
  return abs(x1 - x2) + abs(y1 - y2)
def priorityQueue(queue):
  minFScoreValue = queue[0][1]
  minFScoreObject = queue[0]
  for element in queue:
    if element[1] < minFScoreValue:
      minFScoreValue = element[1]
      minFScoreObject = element
  return minFScoreObject
#Create the grid by iterate over all the possible positions
for i in range(col):
  array = []
  for j in range(row):
    array.append(Box(i, j))
  grid.append(array)
#Set the neighbours for all the boxes
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
          start_box.visited = True
          start_box_set = True
          start_box.g_score = 0
        elif event.button == 3 and not end_box_set:
          i = x // bwidth
          j = y // bheight
          end_box = grid[i][j]
          end_box.end = True
          end_box_set = True
          begin_search = True
          start_box.f_score = calculateH(start_box, end_box)
          queue.append((start_box, start_box.f_score))
          start_box.queue = True
          setObjects.append(start_box)
          for i in range(col):
            for j in range(row):
              grid[i][j].set_neighbours()
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
        current_box = priorityQueue(queue)
        current_box[0].visited = True
        queue.remove(current_box)
        setObjects.remove(current_box[0])
        if current_box[0] == end_box:
          searching = False
          while current_box[0].prior[0] != start_box:
            path.append(current_box[0].prior[0])
            current_box = current_box[0].prior
        for neighbour in current_box[0].neighbours:
          tentative_g_score = current_box[0].g_score + 1
          if tentative_g_score < neighbour.g_score:
            neighbour.prior = current_box
            neighbour.g_score = tentative_g_score
            neighbour.f_score = tentative_g_score + calculateH(neighbour, end_box)
            if not neighbour in queue:
              neighbour.queue = True
              neighbour.prior = current_box
              queue.append((neighbour, neighbour.f_score))
              setObjects.append(neighbour)
      #if queue is 0 and we never found the solution
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
          box.draw(window, (89, 91, 149))
        if box.visited:
          box.draw(window, (44, 60, 116))
        if box in path:
          box.draw(window, (134, 236, 133))
        if box.start:
          box.draw(window, (255, 75, 90))
        if box.end:
          box.draw(window, (255, 231, 129))
        if box.obstacle:
          box.draw(window, (90, 90, 90))
   #Update the display
    pygame.display.flip()
main()
# To do: solve the case when start and end is the same box
