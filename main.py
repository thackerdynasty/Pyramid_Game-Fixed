import pygame
import sys
from pygame.locals import *

from deck import Deck

pygame.init()
size = width, height = (700, 700)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BG_COLOR = (0, 102, 0)

deck = None
board = pygame.sprite.Group()
discard_pile = pygame.sprite.Group()
selectedcard = pygame.sprite.GroupSingle()
next_card = pygame.sprite.GroupSingle()
top_card = pygame.sprite.GroupSingle()
empty_deck = pygame.Rect(0, 0, 71, 94)
empty_deck.bottomleft = (20, height - 20)


def init():
    global deck
    deck = Deck()
    for i in range(7):
        for j in range(i + 1):
            card = deck.deal()
            card.rect.midtop = (width // 2 - 40 * i + 80 * j, 30 + 30 * i)
            card.flip()
            board.add(card)
    next_card.add(deck.deal())
    next_card.sprite.rect.bottomleft = (20, height - 20)


def get_next_card():
    if len(top_card) > 0:
        top_card.sprite.rect.x += 80 + len(discard_pile) * 10
        discard_pile.add(top_card)
    top_card.add(next_card)
    top_card.sprite.flip()
    top_card.sprite.rect.x += 80
    card = deck.deal()
    if card is not None:
        next_card.add(card)
        next_card.sprite.rect.bottomleft = (20,height - 20)
    else:
        next_card.empty()


def check_sprite_clicked(click_point):
    card_clicked = None
    if len(next_card) > 0:
        if next_card.sprite.rect.collidepoint(click_point):
            selectedcard.empty()
            get_next_card()
            return
    for card in board:
        if card.rect.collidepoint(click_point):
            card_clicked = card
    if card_clicked is not None:
        hit_list = pygame.sprite.spritecollide(card_clicked, board, False)
        for card in hit_list:
            if card.rect.y > card_clicked.rect.y:
                return
        card_remove(card_clicked)
        # selectedcard.add(card_clicked)


def card_remove(card_clicked):
    if len(selectedcard) > 0 and selectedcard.sprite.rank + card_clicked.rank == 13:
        selectedcard.sprite.kill()
        card_clicked.kill()
    elif card_clicked.rank == 13:
        card_clicked.kill()
        selectedcard.empty()
    else:
        selectedcard.add(card_clicked)


def main():
    global screen, clock
    init()

    while True:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_f:
                    screen = pygame.display.set_mode(size, FULLSCREEN)
                if event.key == K_d:
                    screen = pygame.display.set_mode(size)
            if event.type == MOUSEBUTTONDOWN:
                click_point = pygame.mouse.get_pos()
                check_sprite_clicked(click_point)

        screen.fill(BG_COLOR)
        board.draw(screen)
        next_card.draw(screen)
        top_card.draw(screen)
        discard_pile.draw(screen)
        if len(next_card) == 0:
            pygame.draw.rect(screen, (204, 173, 0), selectedcard.sprite.rect, 3)
        if len(selectedcard) > 0:
            pygame.draw.rect(screen, (204, 173, 0), selectedcard.sprite.rect, 3)
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
