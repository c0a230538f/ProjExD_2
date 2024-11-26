import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    """
    半透明の黒い画面上に「Game Over」と表示
    引数:screen
    戻り値:なし
    """
    blackbg = pg.Surface((WIDTH, HEIGHT)) #黒背景のSurface
    pg.draw.rect(blackbg, (0, 0, 0) ,(0, 0, WIDTH, HEIGHT)) #黒背景の描画
    pg.Surface.set_alpha(blackbg, 200) #背景の透明化
    screen.blit(blackbg, (0, 0)) #黒背景の表示
    fonto = pg.font.Font(None, 80) #フォントの設定
    txt = fonto.render("Game Over", True, (255, 255, 255)) #ゲームオーバーの文字
    screen.blit(txt, [400, 300]) #ゲームオーバーの表示
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9) #こうかとんの画像
    screen.blit(kk_img, [350, 300]) #左側にこうかとんの表示
    screen.blit(kk_img, [720, 300]) #右側にこうかとんの表示
    pg.display.update() #画面の更新
    time.sleep(5) #5秒待つ

def checkbound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値:真理値タプル（横, 縦）/画面内True, 画面外False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    elif rct.top < 0 or HEIGHT < rct.bottom: #rct.topはこうかとんの頭、bottomは足
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0)) #黒色を透明化
    bb_rct = bb_img.get_rect() #爆弾rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  #
    vx, vy = 5, 5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら、元の場所に戻す
        if checkbound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = checkbound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
