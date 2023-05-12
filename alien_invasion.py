#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'外星人入侵'

_author_='yinhuarong'

import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings=Settings()

        #self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #设置全屏
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            #监视键盘和鼠标事件。
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
                 

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type==pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
    #按键按下动作
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #Q键退出
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()
    
    #松开按键
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #开火动作
    def _fire_bullet(self):
        """创建一个子弹，并将其编入bullets编组中"""
        new_bullet= Bullet(self)
        self.bullets.add(new_bullet)

    #每次循环时都重绘屏幕
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
    #让最近绘制的屏幕可见。
        pygame.display.flip()
    
    def _update_bullets(self):
        self.bullets.update()
    #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人
        alien = Alien(self)
        self.aliens.add(alien)

if __name__=='__main__':
    #创建游戏实例并运行游戏。
    ai=AlienInvasion()
    ai.run_game()