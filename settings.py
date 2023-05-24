#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'设置'

_author_='yinhuarong'

class Settings:
    """存储游戏中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width=400
        self.screen_height=400
        self.bg_color=(230,230,230)
        #飞船设置
        self.ship_speed = 0.5
        self.ship_limit = 3
        #外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        #fleet_direction 1表示右移，-1表示左移。
        self.fleet_direction = 1
        #子弹设置
        self.bullet_speed =1.0
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (60,60,60)