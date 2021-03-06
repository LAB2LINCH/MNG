import random
import time
from pico2d import *
from Bullet.C_EnemyBullet import EBullet
_Bullet = []
class Enemy1:
    PIXEL_PER_METER = (4.0 / 0.3)  # 6 pixel 30 cm
    RUN_SPEED_KMPH = 15 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None

    #_enemy = []

    def __init__(self, PL_X, PL_Y, Enemy_dir, BG_X, BG_Y):
        self.rand = Enemy_dir
        self.type = 1
        self.state = 0
        if self.rand == 0:
            self.x, self.y = random.randint(0, 50), random.randint(0, 1800)
        elif self.rand == 1:
            self.x, self.y = random.randint(3150, 3200), random.randint(0, 1800)
        elif self.rand == 2:
            self.x, self.y = random.randint(0, 3200), random.randint(0, 50)
        elif self.rand == 3:
            self.x, self.y = random.randint(0, 3200), random.randint(1750, 1800)
        #self.sx = self.x - PL_X
        #self.sy = self.y - PL_Y
        self.speed = Enemy1.RUN_SPEED_PPS

        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y

        self.Whattime = 0
        self.alive = 1
        self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        #Enemy1._enemy.append(self)
    def returnx(self):
        return self.x
    def returny(self) :
        return self.y

    def update(self,frame_time, PL_X, PL_Y, _BG_X , _BG_Y):
        if self.x > 3200:
            self.x = 3200
            self.xdir *= -1
        if self.x < 0:
            self.x = 0
            self.xdir *= -1
        if self.y > 1800:
            self.y = 1800
            self.ydir *= -1
        if self.y < 0:
            self.y = 0
            self.ydir *= -1
        self.Whattime +=frame_time

#
        self.x += self.speed * self.xdir * frame_time
        self.y += self.speed * self.ydir * frame_time
        self.sx = self.x - _BG_X
        self.sy = self.y - _BG_Y



        #self.delete_object(_Bullet)

    #def get_list():
    #    return (Enemy1._enemy)
    def ADD_Bullet(self):
        if self.Whattime >= 2.0:
            self.Whattime = 0
            return True




    def draw(self):

        pass

    def draw_bb(self):
        pass
    def get_bb(self):
        pass
