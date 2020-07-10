import pygame
import sys 
import random
import pygame_menu 
pygame.init()

SIZE_BLOCK = 20 # razmer blocov 
FRAME_COLORE = (0,255,204)# cvet okna
BLUE = (0,51,204)
RED = (224,0,0)
WHITE = (255,255,255)
SNAKE_COLORE = (0,102,0)
COUNT_BLOCKS = 20
SPACE = 1
HEADER_COLORE = (0,204,153) # cvet otstupa
HEADER_SPACE = 70 # otstup dlya ballov
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + SPACE * COUNT_BLOCKS, 
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + SPACE * COUNT_BLOCKS + HEADER_SPACE] # razmer okna

screen = pygame.display.set_mode (size) #okno
pygame.display.set_caption('Snake Beksultan') # naz okna
timer = pygame.time.Clock() # 4to by podkl tick (skolko dviz v sekundu)
shrift = pygame.font.SysFont('courier',30)  # v skobkah ukazan nazvanie i razmer srifta

class Snakeblocks:     #class bolkov zmeiki
     def __init__(self,x,y):   #peredaem koordinaty blokov 
         self.x = x
         self.y = y
     def inside_box (self):      # metod ne vypuskaet zmeiku
         return 0 <= self.x <COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS
     def __eq__(self, other):    #sravnennie obetov classa
         return isinstance(other,Snakeblocks) and  self.x == other.x and self.y == other.y
          

def my_blocks (color,row,column): ## function dlya sozdanie blokov
     pygame.draw.rect(screen,color,[SIZE_BLOCK + column * SIZE_BLOCK + SPACE*(column+1),
                                             HEADER_SPACE + SIZE_BLOCK +row *SIZE_BLOCK+ SPACE*(row+1),SIZE_BLOCK,SIZE_BLOCK])


  

def start_the_game():
    def random_emptyblock():      #4to by eda spavnilas randomnyh mestah na karte
        x = random.randint(0,COUNT_BLOCKS-1)
        y = random.randint(0,COUNT_BLOCKS-1)
        empty_block = Snakeblocks(x , y)
        while empty_block in snakebl:   # 4to by golova zmeiki ne menyala cvet
            empty_block.x = random.randint(0,COUNT_BLOCKS-1)
            empty_block.y = random.randint(0,COUNT_BLOCKS-1)
        return empty_block  


    snakebl = [Snakeblocks(8,8),Snakeblocks(8,9),Snakeblocks(8,10)]  #list zmeiki sostoyashih iz blokov 
    meal = random_emptyblock() # randomnoe mesto
    d_row = 0   # dvizh po stroke
    d_column = 1 # dvizh po colonam blokov
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ('EXIT')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_column!=0 :
                    d_row = -1
                    d_column = 0  
                elif event.key == pygame.K_DOWN and d_column!=0:
                    d_row = 1
                    d_column = 0
                elif event.key == pygame.K_LEFT and d_row!=0:
                    d_row = 0
                    d_column = -1
                elif event.key == pygame.K_RIGHT and d_row!=0:
                    d_row = 0
                    d_column = 1


        screen.fill(FRAME_COLORE)#peredali cvet 
        pygame.draw.rect(screen,HEADER_COLORE,[0,0,size[0],HEADER_SPACE])
        text_total = shrift.render(f"Total: {total} ", 0,WHITE)  # o4ki nabrannye za vremya igry
        text_speed = shrift.render(f"Total: {speed} ", 0,WHITE)  # skorost zmeiki
        screen.blit(text_total, (SIZE_BLOCK , SIZE_BLOCK)) # vyvod o4kov
        screen.blit(text_speed, (SIZE_BLOCK + 200 , SIZE_BLOCK)) # vyvod skorosti ewe dobavil 200 ctoby slitno ne bylo

        for row in range (COUNT_BLOCKS):
            for column in range (COUNT_BLOCKS):
                if (row + column)% 2 == 0:
                 color = BLUE
                else :
                 color = WHITE   

                my_blocks(color,row,column)
                            
                #pygame.draw.rect(screen,color,[SIZE_BLOCK + column * SIZE_BLOCK + SPACE*(column+1),
                    #HEADER_SPACE + SIZE_BLOCK +row *SIZE_BLOCK+ SPACE*(row+1),SIZE_BLOCK,SIZE_BLOCK])
        
        head = snakebl[-1] # konec lista GOLOVA
        if not head.inside_box() :  #esli ne v etom predele to vihodit
            print ('GAME OVER')
            pygame.quit()
            sys.exit()
        
        my_blocks(RED, meal.x, meal.y)

        for block in snakebl:
            my_blocks(SNAKE_COLORE, block.x, block.y)
            
        

        if meal == head :
            total += 1   #sravnivaem block golovy i edy
            speed = total // 5 + 1 # skorost budet uvelichivatsya siedinom kazhdim 5tom yablokom 
            snakebl.append(meal)   # dobavlyaem block ewe k zmeike
            meal = random_emptyblock()
        
        new_head = Snakeblocks(head.x + d_row, head.y + d_column) #dvizhenie dealaetsya za chet togo
        snakebl.append(new_head)                                  #я добавляю новую голову змеи каждый раз убирая его хвост
        snakebl.pop(0)
        
        pygame.display.flip() # vyvod okna 
        timer.tick(3 + speed) #ckok kadrov v sekundu skorost perem bloka 
    

menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Name :', default='Player 1')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)