import random
from Background.C_BG import BackGround
from pico2d import *
font = None
class EBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    _eBullet = []
    def __init__(self,E_x, E_y):
        global font
        self.shooter = 1
        self._Bg = BackGround
        self.x = E_x
        self.y = E_y

        self.speed = 0
        self.alive =1
        EBullet._eBullet.append(self)

    def get_distance(self,PL_X, PL_Y):
        dx = self.x - PL_X
        dy = self.y - PL_Y
        return (dx*dx)+(dy*dy)
    def set_dir(self,PL_X, PL_Y):
        if (PL_X < self.x):
            self.xdir = -math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
            self.ydir = -math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        else:
            self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
            self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
    def update(self,frame_time):
        self.speed = EBullet.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir
        if self.x >3200 :
            self.alive = 0
        if self.x < 0 :
            self.alive = 0
        if self.y >1800 :
            self.alive = 0
        if self.y <0 :
            self.alive = 0


    def draw(self):
        self.image.draw(self.sx, self.sy)
#        self.image.draw(self.sx, self.sy)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10
        #return self.sx-10 , self.sy-10, self.sx+10, self.sy+10
    def get_list():
        return (EBullet._eBullet)

def collide(left_a, bottom_a,right_a, top_a, left_b, bottom_b,right_b, top_b):

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
