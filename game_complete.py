import pygame, math, time, os
import random  # 이 부분을 추가

# 나머지 코드는 그대로 유지


#pygame초기화
pygame.init()
pygame.mixer.init()
pygame.font.init()

#창크기
w = 900
h = w * (9/16)
#화면 만들기


clock=pygame.time.Clock()

main = True
ingame = False
running=True
#눌렸나?의 값
keys=[0,0,0,0]
keyset=[0,0,0,0]
maxframe=60
fps=0
#시간 계산위함
gst=time.time()
CTime= time.time()-gst
ty=0#노트y
tst=CTime#노트소환시간
t1=[]
t2=[]
t3=[]
t4=[]

#리듬게임 배경리스트
Rhythm_View = [
    "Background/Desert_bg.png",
    "Background/Winter_bg.png",
    "Background/Volcano_bg.png",
    "Background/Devil_bg.png"
]

Rhythm_View_index = 0

#노래 리스트
music = [
    "music/Desert.mp3",
    "music/Winter.mp3",
    "music/Volcano.mp3",
    "music/Devil.mp3"
]
#music index
music_index = 0

#각 스테이지 음악 시간
game_duration = [
    96,
    124,
    149,
    121
]
#각 스테이지 음악 시간 인덱스
game_duration_index = 0

note_interval = 2

Cpath=os.path.dirname(__file__)
Fpath=os.path.join(Cpath,"font")

rate="PERFEXT"
global stage
stage=1
ingame_font_rate=pygame.font.Font(os.path.join(Fpath,"ingame_font.ttf"),int(w/23))
rate_text=ingame_font_rate.render(str(rate),False,(255,255,255))
speed=2 
notesumt=0
a=0
spin=0
combo=0
combo_effect=0
combo_effect2=0
miss_anim=0
last_combo=0
combo_time=CTime+1
rate_data=[0,0,0,0]
s=stage-1#색 번호
r1=[255,204,255,000]
g1=[204,255,204,000]
b1=[153,255,204,000]#노트 떨어지는 부분/오른 3

r2=[102,178,204,24]
g2=[51,204,61,0]
b2=[0,255,61,84]#버튼있는 부분 네모/그 위ㄱ

r3=[204,51,204,000]
g3=[153,000,0,000]
b3=[102,204,0,000]#오른쪽 

r4=[51,103,102,255]
g4=[000,153,000,255]
b4=[000,255,000,255]#가장진함
screen = pygame.display.set_mode((500, 625))

# pygame.time.get_ticks() = 경과된 시간을 추적
# game_duration_seconds = 리듬 게임을 플레이 시간
start_time = pygame.time.get_ticks()
game_duration_seconds = 0

#Next 버튼 설정
button_rect = pygame.Rect(368, 570, 100, 30)  # 버튼의 위치와 크기를 조절하세요
button_color = (000, 255, 204)  # 버튼의 색상을 조절하세요
button_font = pygame.font.Font(None, 24)
button_text = button_font.render(">>>Next", True, (0, 0, 0))  # 버튼의 텍스트와 색상을 조절하세요

#Start 버튼 설정
start_button_rect = pygame.Rect(150, 120, 60, 30)  # 버튼의 위치와 크기를 조절하세요
start_button_color = (255, 204, 51)  # 버튼의 색상을 조절하세요
start_button_font = pygame.font.Font(None, 24)
start_button_text = button_font.render("Start !", True, (0, 0, 0))  # 버튼의 텍스트와 색상을 조절하세요

start_color_x=[150,330,120,310]
start_color_y=[120,202,353,485]

def load_image(image_path):
    return pygame.image.load(image_path)

#스토리창 사이즈로 돌려놓는 함수
def story_screen_size():
    screen = pygame.display.set_mode((500, 625))

def screen_size():
    screen = pygame.display.set_mode((w, h))
    global s
    s=stage-1#색 번호
font = pygame.font.Font(os.path.join(Fpath,"ingame_font.ttf"),int(w/23))
black=(0, 0, 0)
white=(255,255,255)
judgments = {
    "Perfect",
    "Great",
    "Good",
    "Bad",
    "Worst"
}
def show_result(score, judgments):
    screen.fill(white)

    # 결과 텍스트 생성
    text = font.render("game over! score: {}".format(score), True, black)
    text_rect = text.get_rect(center=(w // 2, h // 2 - 50))
    screen.blit(text, text_rect)

    pygame.display.flip()

    
    pygame.time.delay(4000)

current_image_index = 0
count = 0

image_paths = [
    "image/1.PNG",
    "image/2.PNG",
    "image/3.PNG",
    "image/4.PNG",
    "image/5.PNG", 
    "image/6.PNG", 
    "image/7.PNG", 
    "image/8.PNG", 
    "image/9.PNG", 
    "image/stage_map.png",
    "image/10.PNG", 
    "image/11.PNG",
    "image/12.PNG",
    "image/13.PNG",
    "image/14.PNG",
    "image/15.PNG",
    "image/16.PNG",
    "image/17.PNG",
    "image/18.PNG",
    "image/19.PNG",
    "image/20.PNG",
    "image/21.PNG",
    "image/22.PNG",
    "image/23.PNG",
    "image/24.PNG",
    "image/25.PNG"
]

current_image = load_image(image_paths[current_image_index])
image_change_area = pygame.Rect(368, 570, 100, 100)
stage_star_area=pygame.Rect(150, 120, 60, 30)

running = True

score=0
def rating(n,note_list):
        global combo,miss_anim,last_combo,combo_effect,combo_effect2,combo_time,rate,Bad_count,Miss_count,Good_count,Great_count,Perfect_count,score
        if abs(h/12)*9-rate_data[n-1]<950*speed*(h/900) and (h/12)*9-rate_data[n-1]>=200*speed*(h/900):
           last_combo=combo
           combo+=1
           miss_anim=1
           combo_effect=0.2

           combo_time=CTime+1
           combo_effect2=1.3
           rate="Worst"
           Miss_count += 1

           del note_list[0]
        if abs(h/12)*9-rate_data[n-1]<200*speed*(h/900) and (h/12)*9-rate_data[n-1]>=100*speed*(h/900):
            last_combo=combo
            combo+=1
            miss_anim=1
            combo_effect=0.2
            combo_time=CTime+1
            combo_effect2=1.3
            rate="Bad"
            score+=50

            del note_list[0]
        if abs(h/12)*9-rate_data[n-1]<100*speed*(h/900) and (h/12)*9-rate_data[n-1]>=50*speed*(h/900):
            last_combo=combo
            combo+=1
            miss_anim=1
            combo_effect=0.2
            combo_time=CTime+1
            combo_effect2=1.3
            rate="Good"
            score += 100

            del note_list[0]
        if abs(h/12)*9-rate_data[n-1]<50*speed*(h/900) and (h/12)*9-rate_data[n-1]>=15*speed*(h/900):
            last_combo=combo
            combo+=1
            miss_anim=1
            combo_effect=0.2
            combo_time=CTime+1
            combo_effect2=1.3
            rate="Great"
            score += 200

            del note_list[0]
        if abs(h/12)*9-rate_data[n-1]<15*speed*(h/900) and (h/12)*9-rate_data[n-1]>=0*speed*(h/900):
            last_combo=combo
            combo+=1
            miss_anim=4
            combo_effect=0.2
            combo_time=CTime+1
            combo_effect2=1.3
            rate="PERFECT"
            score+=300
            del note_list[0]

        
        
def sum_note(n):
    if n==1:
        ty=0
        tst=CTime+2
        t1.append([ty,tst])
        
    if n==2:
        ty=0
        tst=CTime+2
        t2.append([ty,tst])
        
    if n==3:
        ty=0
        tst=CTime+2
        t3.append([ty,tst])
        
    if n==4:
        ty=0
        tst=CTime+2
        t4.append([ty,tst])    
        
running = True

while main:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # "25.PNG" 이미지일 때 Next 버튼을 누르면 게임 종료
                if image_paths[current_image_index] == "image/25.PNG" and button_rect.collidepoint(mouse_x, mouse_y):
                    running = False
                    pygame.quit()
    
                if image_change_area.collidepoint(mouse_x, mouse_y) and count !=9:
                    # 마우스 클릭으로 이미지 변경
                    current_image_index = (current_image_index + 1) % len(image_paths)
                    current_image = load_image(image_paths[current_image_index])
                    count += 1
                if count==9 and stage_star_area.collidepoint(mouse_x,mouse_y):
                    # 리듬 게임 시작 시간을 현재 시간으로 업데이트
                    start_time = pygame.time.get_ticks()
                    # 음악 파일의 경로
                    pygame.mixer.music.load(music[music_index])
                    #(-1) = 무한루프를 뜻함
                    pygame.mixer.music.play(-1)
                    running=False
                    next_note_time = 0
                    pygame.init()
                    ingame=True
                    #image2 = pygame.image.load('1.png')
                    image_bg = pygame.image.load(Rhythm_View[Rhythm_View_index])

                    game_duration_seconds = game_duration[game_duration_index]
                    end_time = start_time + (game_duration_seconds * 1000)  # 밀리초 단위로 변환

            
                    
                    screen_size()
        pygame.display.flip()            
                

        screen.fill((0, 0, 0))

        screen.blit(current_image, (0, 0))
        if count!=9:
            pygame.draw.rect(screen, button_color, button_rect)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
        else:
            pygame.draw.rect(screen, start_button_color, start_button_rect)
            screen.blit(start_button_text, (start_button_rect.centerx - start_button_text.get_width() // 2, start_button_rect.centery - start_button_text.get_height() // 2))

        pygame.display.flip()


    while ingame:
        if len(t1)>0:
            rate_data[0]=t1[0][0]   
        if len(t2)>0:
            rate_data[1]=t2[0][0]  
        if len(t3)>0:
            rate_data[2]=t3[0][0]  
        if len(t4)>0:
            rate_data[3]=t4[0][0]  
        if CTime > next_note_time:
            next_note_time = CTime + note_interval  # 다음 노트 생성 시간 업데이트
            note_number = random.randint(1, 4)  # 노트 번호를 1에서 4 사이에서 랜덤하게 선택
            sum_note(note_number)

        # 게임이 시작된 후 경과된 시간 계산 (밀리초 단위)
        CTime = pygame.time.get_ticks() - start_time
        # 게임이 지정된 시간을 초과하면 ingame 모드를 종료하고 다시 stage_map.png 화면으로 돌아감
        if CTime > game_duration_seconds * 1000:
            stage += 1
            if stage <=4:
                a += 1
                speed += 1
                note_interval -= 0.5
                Rhythm_View_index += 1
                game_duration_index += 1
                music_index+=1
                show_result(score, judgments)
                story_screen_size()
                s=stage - 1
                running = True
                ingame = False
                pygame.init()
                pygame.mixer.music.stop()
                start_button_rect = pygame.Rect(start_color_x[a], start_color_y[a], 60, 30)  # 버튼 위치 업데이트
                stage_star_area=pygame.Rect(start_color_x[a], start_color_y[a], 60, 30)
                start_time = pygame.time.get_ticks()  # 시작 시간 초기화
            else:
                count=10
                screen = pygame.display.set_mode((500, 625))
                current_image_index = (current_image_index + 1) % len(image_paths)
                current_image = load_image(image_paths[current_image_index])
                running = True
                ingame = False
                pygame.init()
                pygame.mixer.music.stop()

        CTime = time.time() - gst
        fps=clock.get_fps()
        ingame_font_combo = pygame. font.Font (os.path. join(Fpath,"ingame_font.ttf"),int((w / 38) * combo_effect2))
        combo_text = ingame_font_combo.render(str(combo), False,(255,255,255))
        combo_text_rect = combo_text.get_rect()
        combo_text_rect.center = (w / 2, (h / 12) * 4 + combo_text.get_height() / 2)

        rate_text = ingame_font_rate. render(str(rate), False, (255,255, 255))
        rate_text = pygame. transform. scale(rate_text, (int (w / 110 * len(rate) * combo_effect2), int((w / 58 * combo_effect * combo_effect2))))
        ingame_font_miss = pygame. font.Font(os.path.join(Fpath, "ingame_font.ttf"),int ((w / 38 * miss_anim)))
        miss_text = ingame_font_miss. render (str(last_combo), False, (255, 0, 0))

        
        if fps==0:
            fps=maxframe
        #겜 끄는거
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                ingame = False
                pygame.mixer.music.stop()
                pygame.quit()
            

            #누르면 참 거짓으로 변경
            if event.type == pygame.KEYDOWN:
                #'r'키가 눌렸는지 확인
                if event.key == pygame.K_r: 
                    
                    stage += 1
                    show_result(score, judgments)
                    
                    
                    if stage<=4:
                        a += 1
                        speed += 1
                        note_interval -= 0.5
                        Rhythm_View_index += 1
                        game_duration_index += 1
                        music_index+=1
                        screen = pygame.display.set_mode((500, 625))
                        s=stage - 1
                        running = True
                        ingame = False
                        pygame.init()
                        pygame.mixer.music.stop()
                        start_button_rect = pygame.Rect(start_color_x[a], start_color_y[a], 60, 30)  # 버튼 위치 업데이트
                        stage_star_area=pygame.Rect(start_color_x[a], start_color_y[a], 60, 30)
                    else:
                        count=10
                        current_image_index = (current_image_index + 1) % len(image_paths)
                        current_image = load_image(image_paths[current_image_index])
                        screen = pygame.display.set_mode((500, 625))
                        running = True
                        ingame = False
                        pygame.init()
                        pygame.mixer.music.stop()
                    
                if event.key == pygame.K_d:
                    keyset[0] = 1
                    
                    if len(t1)>0:
                        if t1[0][0]>h/2:
                            rating(1,t1)
                            
                        else:
                            last_combo=0
                            combo=0
                            miss_anim=1
                            combo_effect=0.2
                            combo_time=CTime+1
                            combo_effect2=1.3
                            rate="miss"
                            
                if event.key == pygame.K_f:
                    keyset[1] = 1
                    
                    if len(t2)>0:
                        if t2[0][0]>h/2:
                            rating(2,t2)
                            
                        else:
                            last_combo=0
                            combo=0
                            miss_anim=1
                            combo_effect=0.2
                            combo_time=CTime+1
                            combo_effect2=1.3
                            rate="miss"
                            
                if event.key == pygame.K_j:
                    keyset[2] = 1
                    
                    if len(t3)>0:
                        if t3[0][0]>h/2:
                            rating(3,t3)
                            
                        else:
                            last_combo=0
                            combo=0
                            miss_anim=1
                            combo_effect=0.2
                            combo_time=CTime+1
                            combo_effect2=1.3
                            rate="miss"
                            
                        
                if event.key == pygame.K_k:
                    keyset[3] = 1
                    
                    if len(t4)>0:
                        if t4[0][0]>h/2:
                            rating(4,t4)
                            
                        else:
                            last_combo=0
                            combo=0
                            miss_anim=1
                            combo_effect=0.2
                            combo_time=CTime+1
                            combo_effect2=1.3
                            rate="miss"
                            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    keyset[0] = 0
                if event.key == pygame.K_f:
                    keyset[1] = 0
                if event.key == pygame.K_j:
                    keyset[2] = 0
                if event.key == pygame.K_k:
                    keyset[3] = 0
        #바탕화면
        screen.fill((r3[s], g3[s], b3[s]))
        screen.blit(image_bg,(0,0))
        #감속?인듯
        keys[0] += (keyset[0] - keys[0]) / (2 * (maxframe / fps))
        keys[1] += (keyset[1] - keys[1]) / (2 * (maxframe / fps))
        keys[2] += (keyset[2] - keys[2]) / (2 * (maxframe / fps))
        keys[3] += (keyset[3] - keys[3]) / (2 * (maxframe / fps))

        #텍스트 움직임
        if CTime>combo_time:
            combo_effect+=(0-combo_effect)/(7*(maxframe/fps))
        if CTime<combo_time:
            combo_effect+=(1-combo_effect)/(7*(maxframe/fps))
        combo_effect2+=(2-combo_effect2)/(7*maxframe/fps)

        miss_anim+=(4-miss_anim)/(14*(maxframe/fps))
        #pygame.draw.rect(screen, (r1[s], g1[s], b1[s]), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w / 50)))  # 기어 배경
        #노트 누르면 똥똥똥 보임
        
        for i in range(7):
            i += 1
            if s in [0,1,2]:  # s 값이 0에서 3 사이일 때 흰색에서 검정색으로
                color = (255 - ((255 / 7) * i), 255 - ((255 / 7) * i), 255 - ((255 / 7) * i))
            elif s == 3:  # s 값이 4일 때 빨간색에서 검정색으로
                color = (255 - ((255 / 7) * i), 0, 0)

            # 사각형을 그리는 코드에서 이 색상을 사용
            pygame.draw.rect(screen, color, (w / 2 - w / 8 + w / 32 - (w / 32) * keys[0], (h / 12) * 9 - (h / 30) * keys[0] * i, w / 16 * keys[0], (h / 35) / i))
            pygame.draw.rect(screen, color, (w / 2 - w / 16 + w / 32 - (w / 32) * keys[1], (h / 12) * 9 - (h / 30) * keys[1] * i, w / 16 * keys[1], (h / 35) / i))
            pygame.draw.rect(screen, color, (w / 2 + w / 32 - (w / 32) * keys[2], (h / 12) * 9 - (h / 30) * keys[2] * i, w / 16 * keys[2], (h / 35) / i))
            pygame.draw.rect(screen, color, (w / 2 + w / 16 + w / 32 - (w / 32) * keys[3], (h / 12) * 9 - (h / 30) * keys[3] * i, w / 16 * keys[3], (h / 35) / i))

        ##노트 생성하고 떨어뜨림
        for tile_data in t1:
            tile_data[0] = (h / 12) * 9 + (CTime - tile_data[1]) * 350 * speed * (h / 900)
            pygame. draw. rect (screen, (255, 255, 255), (w / 2 - w / 8, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo=0
                combo=0
                miss_anim=1
                combo_effect=0.2
                combo_time=CTime+1
                combo_effect2=1.3
                rate="miss"
                t1. remove(tile_data)
        for tile_data in t2:
            tile_data[0] = (h / 12) * 9 + (CTime - tile_data[1]) * 350 * speed * (h / 900)
            pygame. draw. rect (screen, (255, 255, 255), (w / 2 - w / 16, tile_data[0] - h / 100, w / 16, h / 50))#노트 색?
            if tile_data[0] > h - (h / 9):
                last_combo=0
                combo=0
                miss_anim=1
                combo_effect=0.2
                combo_time=CTime+1
                combo_effect2=1.3
                rate="miss"
                
                t2. remove(tile_data)
        for tile_data in t3:
            tile_data[0] = (h / 12) * 9 + (CTime - tile_data[1]) * 350 * speed * (h / 900)
            pygame. draw. rect (screen, (255, 255, 255), (w / 2 , tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo=0
                combo=0
                miss_anim=1
                combo_effect=0.2
                combo_time=CTime+1
                combo_effect2=1.3
                rate="miss"
                t3. remove (tile_data)
        for tile_data in t4:
            tile_data[0] = (h / 12) * 9 + (CTime - tile_data[1]) * 350 * speed * (h / 900)
            pygame. draw. rect (screen, (255, 255, 255), (w / 2+ w / 16, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo=0
                combo=0
                miss_anim=1
                combo_effect=0.2
                combo_time=CTime+1
                combo_effect2=1.3
                rate="miss"
                t4. remove (tile_data)    
        
        #그 누르는 부분 선
        pygame.draw.rect(screen, (r2[s], g2[s], b2[s]), (w/2-w/8,(h/12)*9,w/4,h/2))#진한 갈색부분
        #screen.blit(image2, (w/2 - w/8, 0))
        pygame.draw.rect(screen, (r4[s], g4[s], b4[s]), (w/2-w/8,(h/12)*9,w/4,h/2),int(h/100))#판정 선

       #태두리선     
        pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w / 50)), int(w / 100))  # 기어 라인

        pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], 255 - 100 * keys[0]), (w / 2 - w / 9, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
        pygame.draw.rect(screen, (255 - 100 * keys[3],255 - 100 * keys[3], 255 - 100 * keys[3]), (w / 2 + w / 13.5, (h / 24) * 19 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))

        pygame.draw.circle(screen, (150, 150, 150), (w / 2, (h / 24) * 21), (w / 20), int(h / 200))
        pygame.draw.line(screen, (150, 150, 150), (w / 2 - math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)), (w / 2 + math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))
        spin += (speed / 20 * (maxframe / fps))


        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 - w / 18, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))

        pygame.draw.rect(screen, (255 - 100 * keys[2], 255 - 100 * keys[2], 255 - 100 * keys[2]), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 + w / 58, (h / 48) * 43 + (h / 48) * (keys[2] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))
        if rate=="miss":
            miss_text.set_alpha(255-(255/4)*miss_anim)
        else:
            miss_text.set_alpha(0)

        screen.blit(combo_text, combo_text_rect)
        screen.blit(rate_text, (w/2 - rate_text.get_width()/2, (h/12)*8 + rate_text.get_height()/2))
        screen.blit(miss_text, combo_text_rect)
        
        pygame.display.flip()
        clock.tick(maxframe)