import numpy as np
import cv2 as cv
import random

# general parameters
width = 900
height = 600
n_trees = 30
ground_level = height-100

# colours
green, light_green, brown = (40,185,40),(25,220,0),(30,65,155)

# blank image
bg = np.zeros((height, width, 3), dtype=np.uint8)

# draw background
cv.rectangle(bg,(width,0), (0, ground_level), (255,225,95), -1)
cv.rectangle(bg,(width, ground_level), (0, height), green, -1)

# ***************
class Tree:
    def __init__(self, image, location):
        self.img = image
        self.loc = location
        self.ht = 300
        self.radius = 100
    def draw(self):
        # trunk
        cv.line(self.img, (self.loc,ground_level), (self.loc,ground_level-self.ht), brown, 20)
        #leafs
        cv.circle(self.img, (self.loc,ground_level-self.ht), self.radius, green, -1)
        cv.circle(self.img, (self.loc - 90, ground_level - self.ht+self.radius-40), self.radius-40, green, -1)
        cv.circle(self.img, (self.loc + 90, ground_level - self.ht + self.radius - 40), self.radius - 40, green, -1)
        return self.img
# ***************

#display image
img = Tree(bg, 450).draw()
cv.imshow('forest of objects', img)

cv.waitKey(0)
cv.destroyAllWindows()