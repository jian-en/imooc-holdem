# -*- coding: utf-8 -*-

import random
import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('德州扑克')


GREEN = 0, 100, 0
GAP = 100

RANK_REP = '-A23456789TJQK'
NUMBERS = range(1, 14)
PATTERNS = ('c', 'd', 'h', 's')
BACK_CARD = pygame.image.load("images/back.gif")
CARD_W, CARD_H = BACK_CARD.get_rect().width, BACK_CARD.get_rect().height

status, cards, full, message = None, None, None, ''
wins, loses, draws = 0, 0, 0

def reset_game():
    global status, cards, full, message
    status = 1
    cards = {"you": [],
            "three": [],
            "fourth": [],
            "fifth": [],
            "I": []}
    full = [(number, pattern) for number in NUMBERS for pattern in PATTERNS]
    random.shuffle(full)
    message = ''

def message_display(text, location):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = location
    screen.blit(TextSurf, TextRect)

def score(wins, loses, draws):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Wins: %s | Loses: %s | Draws: %s' % (wins, loses, draws), True, (0, 0, 0))
    screen.blit(text, (550, 10))

def generate_img_path(number, pattern):
    return "images/%02d%s.gif" % (number, pattern)

def select_one_card(back=False):
    global full
    number, pattern = full.pop()
    return RANK_REP[number] + pattern.upper(), BACK_CARD if back else pygame.image.load(generate_img_path(number, pattern))

def draw(num, start_x, y, category, invisible=False):
    rect = pygame.Rect(0, 0, CARD_W, CARD_H)
    for i in range(num):
        rect.center = (start_x + GAP * i, y)
        try:
            _, img = cards[category][i]
        except IndexError:
            rep, img = select_one_card(invisible)
            cards[category].append((rep, img))
        screen.blit(img, rect)

def flip(cards):
    i = 0
    for rep, sprite in cards:
        number, pattern = RANK_REP.index(rep[0]), rep[1].lower()
        img = pygame.image.load(generate_img_path(number, pattern))
        rect = sprite.get_rect()
        rect.center = (350 + GAP * i, 110)
        screen.blit(img, rect)
        i += 1


def who_wins(cards):
    global wins, loses, draws
    my_hands, you_hands, comm_hands = [], [], []
    for k, v in cards.items():
        reps = [i[0] for i in v]
        if k == 'I':
            my_hands += reps
        elif k == 'you':
            you_hands += reps
        else:
            comm_hands += reps

    from seven import best_hand_one
    from poker import poker
    my_best = best_hand_one(my_hands, comm_hands)
    you_best = best_hand_one(you_hands, comm_hands)
    winner = poker([my_best, you_best])

    if len(winner) == 1 and set(winner[0]) == set(my_best):
        return 1, 0, 0
    elif len(winner) == 1 and set(winner[0]) == set(you_best):
        return 0, 1, 0
    else:
        return 0, 0, 1

clock = pygame.time.Clock()
reset_game()

def increase_status():
    global status
    status += 1

def quit_game():
    pygame.quit()
    quit()

def fold_game():
    global loses, status
    if status > 1:
        loses += 1
    reset_game()


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.color = ic
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        screen.blit(textSurf, textRect)

    def clicked(self, click_x, click_y):
        if self.x + self.w > click_x > self.x and self.y + self.h > click_y > self.y:
            return True
        return False

    def invoke(self):
        self.action()

    def inactive(self):
        self.color = self.ic

    def active(self):
        self.color = self.ac


bet_button = Button('Bet', 650, 450, 100, 50, (0, 0, 200), (0, 0, 255), increase_status)
fold_button = Button('Fold', 650, 500, 100, 50, (200, 200, 0), (255, 255, 0), fold_game)
quit_button = Button('Quit', 650, 550, 100, 50, (200, 0, 0), (255, 0, 0), quit_game)
buttons = [bet_button, fold_button, quit_button]

message = ''

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.clicked(pos[0], pos[1]):
                    button.invoke()
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.clicked(pos[0], pos[1]):
                    button.active()
                else:
                    button.inactive()

    screen.fill(GREEN)
    bet_button.draw(screen)
    quit_button.draw(screen)
    fold_button.draw(screen)

    message_display(message, (WIDTH / 2, 20))
    score(wins, loses, draws)

    message_display(message, (WIDTH / 2, 20))
    score(wins, loses, draws)

    if status >= 2:
        draw(2, 350, 110, "you", invisible=True)
        draw(2, 350, 510, "I")
    if status >= 3:
        draw(3, 200, 310, "three")
    if status >= 4:
        draw(1, 500, 310, "fourth")
    if status >= 5:
        draw(1, 600, 310, "fifth")

    if status >= 6:
        flip(cards['you'])
        result = who_wins(cards)
        if result[0]:
            message = 'You win!'
        elif result[1]:
            message = 'You lose!'
        else:
            message = 'Draw!'

    if status >= 7:
        wins += result[0]
        loses += result[1]
        draws += result[2]
        reset_game()

    pygame.display.update()  # flip()
    clock.tick(40)
