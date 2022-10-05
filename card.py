import pygame
from pygame.locals import *

class Card(pygame.sprite.Sprite):

    def __init__(self,suit,rank):
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.faceup = False

        self.images = {
            True: pygame.image.load("cards/{} {}.png".format(suit,rank)),
            False: pygame.image.load("cards/Back Blue 1.png")

        }

        self.image = self.images[self.faceup]
        self.rect = self.image.get_rect()

    def flip(self):
        self.faceup = not self.faceup
        self.image = self.images[self.faceup]

    def draw(self,screen):
        screen.blit(self.image,self.rect)
