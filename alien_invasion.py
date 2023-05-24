#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'外星人入侵'

_author_='yinhuarong'

import sys
from time import sleep

import pygame
from settings import Settings
from game_stats import Gamestats
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
        #创建一个用于存储游戏统计信息的实例。
        self.stats = Gamestats(self)
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            #监视键盘和鼠标事件。
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
                 

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        #ESC键退出
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
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
    #检查是否有子弹击中了外星人。
    #如果是，就删除相应的子弹和外星人。
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            #新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置。"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人
        alien = Alien(self)
        #获取alien图片的宽
        alien_width,alien_height=alien.rect.size
        available_space_x = self.settings.screen_width -(2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #计算屏幕可容纳多少行外星人。
        ship_height = self.ship.rect.height
        available_space_y= (self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows = available_space_y // (2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):

                self._create_alien(alien_number,row_number)
            
    def _create_alien(self,alien_number,row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien_width,alien_height =alien.rect.size
        alien.x = alien_width+ 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            #将ships_left减一
            self.stats.ships_left -= 1
            #清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕的底端中央
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(0.5)
        else:
            self.stats.game_active = False

if __name__=='__main__':
    #创建游戏实例并运行游戏。
    ai=AlienInvasion()
    ai.run_game()