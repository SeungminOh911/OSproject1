import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0, 0), alive=True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        self.alive = False
        # 20% 확률로 아이템 생성
        if random.random() <= 0.2:
            color = random.choice([(255, 0, 0), (0, 0, 255)])  # 빨간색 or 파란색
            item = Item(color, (self.rect.centerx, self.rect.centery))
            return item
        return None


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list, items: list):
        for block in blocks[:]:
            if block.alive and self.rect.colliderect(block.rect):
                item = block.collide()
                if item:
                    items.append(item)  # 아이템 추가
                self.dir = 360 - self.dir
                blocks.remove(block)
                break

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:  # 좌우 벽 충돌
            self.dir = 180 - self.dir  # 공의 진행 방향 반전
        if self.rect.top <= 0:  # 상단 벽 충돌
            self.dir = 360 - self.dir  # 공의 진행 방향 반전

    def alive(self):
        if self.rect.top <= config.display_dimension[1]:
            return True
        else:
            return False


class Item(Basic):
    def __init__(self, color: tuple, pos: tuple):
        super().__init__(color, config.ball_speed / 2, pos, config.item_size)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self):
        self.rect.move_ip(0, self.speed)