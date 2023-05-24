#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'外星人'

_author_='yinhuarong'

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """定义外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 装载飞船图片并获得他的矩形属性.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 在屏幕左上方新建一个外星人.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存放外星人水平位置.
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，则返回true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True