''' ---------- GAME SETTINGS ---------- '''

import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()
import asyncio

win_width = 900
win_height = 600
white = (255,255,255)
black = (0,0,0)
score = 0
lives = 10
player_size = 40
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Moving')

font = pg.font.Font(None, 30)

player_image_R = pg.image.load('./assets/images/marioR.png')
player_image_L = pg.image.load('./assets/images/marioL.png')
player_image_R = pg.transform.scale(player_image_R, (40,55))
player_image_L = pg.transform.scale(player_image_L, (40,55))
player_pos = [win_width / 2, 545]
speed_x = 0
speed_y = 0


obj_size = 60
obj_data = [] 
obj = pg.image.load('./assets/images/e1.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))


heart_size = 60
heart_data = [] 
heart = pg.image.load('./assets/images/heart.png')
heart = pg.transform.scale(heart, (heart_size, heart_size))

bg_image = pg.image.load('./assets/images/background.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:    
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])

def create_heart(heart_data):
    if len(heart_data) < 3 and random.random() < 0.1:    
        x = random.randint(0, win_width - heart_size)
        y = 0                                         
        heart_data.append([x, y, heart])
        
def update_objects(obj_data):
    global score

    for object in obj_data:
        x=0
        y=700
        if score < 25:
            speed = 5
        elif score < 50:
            speed = 8
        else:
            speed = 12
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1

def update_heart(heart_data):

    for heart in heart_data:
        x=0
        y=700
        if score < 25:
            speed = 5
        elif score < 50:
            speed = 8
        else:
            speed = 12
        x, y, image_data = heart
        if y < win_height:
            y += speed
            heart[1] = y
            screen.blit(image_data, (x, y))
        else:
            heart_data.remove(heart)


def collision_check(obj_data, player_pos):
    global running, lives
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            lives -= 1
            obj_data.remove(object)
            if lives == 0:
                running = False
            break


def heart_collision_check(heart_data, player_pos):
    global lives
    for heart in heart_data:
        x, y, image_data = heart
        player_x, player_y = player_pos[0], player_pos[1]
        heart_rect = pg.Rect(x, y, heart_size, heart_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(heart_rect):
            lives += 1
            heart_data.remove(heart)






player_speed = 10
running = True

async def main():

    global running, speed_x, speed_y, player_x, player_y, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:

                

                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    speed_x -= player_speed

                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    speed_x += player_speed

                if event.key == pg.K_UP or event.key == pg.K_w:
                    speed_y -= player_speed

                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    speed_y += player_speed

            speed_x = speed_x*0.34
            speed_y = speed_y*0.34
            if speed_x < 0.03 and speed_x > -0.03:
                speed_x = 0

            if speed_y < 0.03 and speed_y > -0.03:
                speed_y = 0
            player_x,player_y = player_pos[0], player_pos[1]

        player_x += speed_x
        player_y += speed_y
        
        if player_x > 860:
            player_x  = 860
        elif player_x < 0:
            player_x = 0

        if player_y > 545:
            player_y = 545
        elif player_y < 0:
            player_y = 0



        player_pos = [player_x,player_y]
                    

        screen.fill('white')
        screen.blit(bg_image, (0, 0))

        text = f'lives: {lives}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 60))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)
        create_heart(heart_data)
        update_heart(heart_data)
        heart_collision_check(heart_data, player_pos)
        if speed_x < 0:
            screen.blit(player_image_L, (player_pos[0], player_pos[1]))
        else:
            screen.blit(player_image_R, (player_pos[0], player_pos[1]))

        clock.tick(60)
        pg.display.flip()


        await asyncio.sleep(0)

asyncio.run(main())
