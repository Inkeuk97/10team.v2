import pygame
import random
import time
import pygame.mixer

pygame.init() 
pygame.mixer.init()  # 음악 시스템 초기화

# 음악 로딩 및 재생
INITIAL_VOLUME = 0.1
pygame.mixer.music.load("arcade-music.wav")  # 같은 폴더에 있는 파일
pygame.mixer.music.play(-1)  # 무한 반복 재생
pygame.mixer.music.set_volume(INITIAL_VOLUME)  # 0.0 ~ 1.0 볼륨조절

# 효과음 로딩
hit_sound = pygame.mixer.Sound("bounce-paddle.ogg")
hit_sound.set_volume(0.2)  # 볼륨 조절 (0.0 ~ 1.0)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) 

clock = pygame.time.Clock()

# 시작 화면 출력
def show_start_screen():
    sound_on = True
    icon_rect = pygame.Rect(screen_width - 50, screen_height - 50, 40, 40) #아이콘 위치

    # 게임 선택 버튼
    block_button = pygame.Rect(screen_width // 2 - 130, screen_height // 2 + 80, 250, 50)
    snake_button = pygame.Rect(screen_width // 2 - 130, screen_height // 2 + 150, 250, 50)

    while True:
        screen.fill(BLACK)
        title = large_font.render('Classic Games', True, YELLOW)
        instruction = small_font.render('Choose the Game', True, WHITE)
        screen.blit(title, title.get_rect(centerx=screen_width // 2, centery=screen_height // 2 - 80))
        screen.blit(instruction, instruction.get_rect(centerx=screen_width // 2, centery=screen_height // 2 - 30))

        # 버튼 그리기
        pygame.draw.rect(screen, BLUE, block_button)
        pygame.draw.rect(screen, GREEN, snake_button)

        block_text = small_font.render("Block break", True, WHITE)
        snake_text = small_font.render("Block break. Snake", True, WHITE)
        screen.blit(block_text, block_text.get_rect(center=block_button.center))
        screen.blit(snake_text, snake_text.get_rect(center=snake_button.center))

        pygame.draw.rect(screen, GREEN if sound_on else RED, icon_rect)
        icon_text = small_font.render('on' if sound_on else 'off', True, WHITE)
        screen.blit(icon_text, icon_text.get_rect(center=icon_rect.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # 시작 화면에서 ESC 누르면 종료
                elif event.key == pygame.K_SPACE:
                    return 'block', sound_on
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if icon_rect.collidepoint(event.pos):
                    sound_on = not sound_on
                    pygame.mixer.music.set_volume(INITIAL_VOLUME if sound_on else 0.0)
                elif block_button.collidepoint(event.pos):
                    return 'block', sound_on
                elif snake_button.collidepoint(event.pos):
                    return 'snake', sound_on
                

    





import pygame
import random

def runSnakeGame():
    pygame.init()
    WINDOW = 500
    TILE_SIZE = 20

    def init_snake(start_pos, start_dir):
        snake = pygame.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
        snake.center = start_pos
        length = 5
        tail = []
        for i in range(length):
            part = snake.copy()
            part.move_ip(
                -start_dir[0] // abs(start_dir[0]) * TILE_SIZE * i if start_dir[0] != 0 else 0,
                -start_dir[1] // abs(start_dir[1]) * TILE_SIZE * i if start_dir[1] != 0 else 0
            )
            tail.append(part)
        return {'head': tail[0], 'tail': tail, 'dir': start_dir, 'length': length, 'dead': False}

    def spawn_food():
        while True:
            x = random.randint(0, (WINDOW - TILE_SIZE) // TILE_SIZE) * TILE_SIZE
            y = random.randint(0, (WINDOW - TILE_SIZE) // TILE_SIZE) * TILE_SIZE
            food = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            if food.collidelist(snake1['tail'] + snake2['tail']) == -1:
                return food

    screen = pygame.display.set_mode([WINDOW] * 2)
    clock = pygame.time.Clock()
    paused = False

    score1 = 0
    score2 = 0
    WIN_SCORE = 3

    def reset_game():
        snake1 = init_snake((TILE_SIZE * 2, TILE_SIZE * 2), (TILE_SIZE, 0))
        snake2 = init_snake((WINDOW - TILE_SIZE * 2, WINDOW - TILE_SIZE * 2), (-TILE_SIZE, 0))
        dont1 = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
        dont2 = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
        return snake1, snake2, dont1, dont2

    def draw_text_center(text, size, color):
        font = pygame.font.SysFont(None, size)
        render = font.render(text, True, color)
        rect = render.get_rect(center=(WINDOW // 2, WINDOW // 2))
        screen.blit(render, rect)

    def draw_scores(score1, score2):
        font = pygame.font.SysFont(None, 30)
        text1 = font.render(f"Green: {score1}", True, 'green')
        text2 = font.render(f"Blue: {score2}", True, 'blue')
        screen.blit(text1, (10, 10))
        screen.blit(text2, (WINDOW - text2.get_width() - 10, 10))

    snake1, snake2, dont1, dont2 = reset_game()
    food = spawn_food()  # 초기 먹이 생성

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_p:
                    paused = not paused

        if paused:
            screen.fill('black')
            draw_text_center("Paused", 50, 'white')
            pygame.display.flip()
            clock.tick(15)
            continue

        keys = pygame.key.get_pressed()
        # 방향 입력 처리
        if keys[pygame.K_w] and dont1[pygame.K_w]:
            snake1['dir'] = (0, -TILE_SIZE)
            dont1 = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}
        elif keys[pygame.K_s] and dont1[pygame.K_s]:
            snake1['dir'] = (0, TILE_SIZE)
            dont1 = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
        elif keys[pygame.K_a] and dont1[pygame.K_a]:
            snake1['dir'] = (-TILE_SIZE, 0)
            dont1 = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}
        elif keys[pygame.K_d] and dont1[pygame.K_d]:
            snake1['dir'] = (TILE_SIZE, 0)
            dont1 = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}

        if keys[pygame.K_UP] and dont2[pygame.K_UP]:
            snake2['dir'] = (0, -TILE_SIZE)
            dont2 = {pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
        elif keys[pygame.K_DOWN] and dont2[pygame.K_DOWN]:
            snake2['dir'] = (0, TILE_SIZE)
            dont2 = {pygame.K_UP: 0, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
        elif keys[pygame.K_LEFT] and dont2[pygame.K_LEFT]:
            snake2['dir'] = (-TILE_SIZE, 0)
            dont2 = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 0}
        elif keys[pygame.K_RIGHT] and dont2[pygame.K_RIGHT]:
            snake2['dir'] = (TILE_SIZE, 0)
            dont2 = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 0, pygame.K_RIGHT: 1}

        screen.fill('black')

        # 먹이 그리기
        pygame.draw.rect(screen, 'red', food)

        def move_snake(snake):
            if snake['dead']:
                return
            next_head = snake['head'].copy()
            next_head.move_ip(snake['dir'])

            if next_head.left < 0:
                next_head.left = WINDOW - TILE_SIZE
            elif next_head.right > WINDOW:
                next_head.right = 0
            if next_head.top < 0:
                next_head.top = WINDOW - TILE_SIZE
            elif next_head.bottom > WINDOW:
                next_head.bottom = 0

            if next_head.collidelist(snake['tail']) != -1:
                snake['dead'] = True
                return

            snake['head'] = next_head
            snake['tail'].append(next_head.copy())
            if len(snake['tail']) > snake['length']:
                snake['tail'].pop(0)

        move_snake(snake1)
        move_snake(snake2)

        # 먹이 먹었는지 확인
        if snake1['head'].colliderect(food):
            snake1['length'] += 1
            food = spawn_food()

        if snake2['head'].colliderect(food):
            snake2['length'] += 1
            food = spawn_food()

        # 충돌 처리
        if not snake1['dead'] and not snake2['dead']:
            if snake1['head'].center == snake2['head'].center:
                snake1['dead'] = True
                snake2['dead'] = True

        if not snake1['dead']:
            if snake1['head'].collidelist(snake2['tail']) != -1:
                snake1['dead'] = True
        if not snake2['dead']:
            if snake2['head'].collidelist(snake1['tail']) != -1:
                snake2['dead'] = True

        def draw_snake(snake, color):
            for part in snake['tail']:
                pygame.draw.rect(screen, color, part)
            if snake['dead']:
                font = pygame.font.SysFont(None, 40)
                text = font.render("Dead", True, 'red')
                screen.blit(text, text.get_rect(center=snake['head'].center))

        draw_snake(snake1, 'green')
        draw_snake(snake2, 'blue')
        draw_scores(score1, score2)

        pygame.display.flip()
        clock.tick(15)

        if snake1['dead'] or snake2['dead']:
            winner_text = "Draw!"
            if snake1['dead'] and not snake2['dead']:
                winner_text = "Blue Wins!"
                score2 += 1
            elif snake2['dead'] and not snake1['dead']:
                winner_text = "Green Wins!"
                score1 += 1

            screen.fill('black')
            draw_text_center(winner_text, 50, 'yellow')
            pygame.display.flip()
            pygame.time.wait(2000)

            if score1 >= WIN_SCORE:
                screen.fill('black')
                draw_text_center("Green Wins the Game!", 60, 'green')
                pygame.display.flip()
                pygame.time.wait(3000)
                return
            elif score2 >= WIN_SCORE:
                screen.fill('black')
                draw_text_center("Blue Wins the Game!", 60, 'blue')
                pygame.display.flip()
                pygame.time.wait(3000)
                return

            # 게임 리셋 후 먹이도 다시 생성
            snake1, snake2, dont1, dont2 = reset_game()
            food = spawn_food()







def runBrickGame(sound_on):
    
    pygame.mixer.music.set_volume(INITIAL_VOLUME if sound_on else 0.0)

    Level = 1

    paused = False
    
    #게임 상태 및 변수상태 초기화
    score = 0                   #벽돌 깬 횟수 기록 (게임 점수)
    Life = 3                    #생명 (3번 놓치면 게임 오버)
    SUCCESS = 1                 #게임 성공을 나타내는 상태값
    FAILURE = 2                 #게임 실패를 나타내는 상태값
    game_over = 0               #게임 현재상태 (0이면 실행중)

    #벽돌 생성
    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 3               #8열 3행의 벽돌 생성
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 80, 60, 16)           #벽돌의 크기 : 60 * 16 / 벽돌사이 간격 : 가로 10 세로 5 / 열간격 : (60 + 10) / 행간격 : (16 + 5) /  시작좌표 : (35, 35)
            bricks.append(brick)                                                                            #bricks 배열에 추가

    #공과 패들 초기 설정
    ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)                   #공 크기 :16 * 16, 화면 정 중앙에 위치
    ball_dx = 5.0                                                                                             #ball_dx : 공 x축 속도
    ball_dy = -5.0                                                                                            #ball_dy : 공 y축 속도

    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 100, 16)                          #패들 크기 : 80 * 16 / 화면 아래쪽에 위치 시킴
    paddle_dx = 0                                                                                           #패들 좌우 이동속도 (키 입력에 따라 변경)

    #메인루프 시작
    while True: 
        delta_time = clock.tick(60) / 10000                                                                 #FPS 60으로 설정 : 게임속도 고정
        screen.fill(BLACK)                                                                                  #이전 프레임의 내용을 지우고 새로 그림

    #이벤트 처리 (키 입력)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -5.0
                elif event.key == pygame.K_a:
                    paddle_dx = -5.0
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 5.0
                elif event.key == pygame.K_d:
                    paddle_dx = 5.0
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddle_dx = 0
                elif event.key == pygame.K_a:
                    paddle_dx = 0
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 0
                elif event.key == pygame.K_d:
                    paddle_dx = 0


        if not paused and game_over == 0:
        #객체 위치 업데이트
            paddle.left += paddle_dx

            ball.left += ball_dx
            ball.top  += ball_dy

        #공의 벽 충돌 처리
            ##공이 좌우 벽에 닿으면 반사 (방향 반전)
            if ball.left <= 0:
                ball.left = 0
                ball_dx = -ball_dx
            elif ball.left >= screen_width - ball.width: 
                ball.left = screen_width - ball.width
                ball_dx = -ball_dx

            ##공이 천장에 닿으면 위아래 방향 반전
            if ball.top < 0:
                ball.top = 0
                ball_dy = -ball_dy

            ##공이 화면 아래로 떨어지면 Life -= 1 (생명감소)
            ##공을 다시 중앙에 위치시키고 방향만 반대로
            elif ball.top >= screen_height:
                Life -= 1
                ball.left = screen_width // 2 - ball.width // 2
                ball.top = screen_height // 2 - ball.width // 2
                ball_dy = -ball_dy 

        #게임 오버 조건 검사
            if Life <= 0:
                game_over = FAILURE                                                                         #공을 3번 놓치면 게임 실패 처리

        #패들의 화면 경계 제한 (패들이 화면 밖으로 나가지 않게 함)
            if paddle.left < 0:
                paddle.left = 0
            elif paddle.left > screen_width - paddle.width:
                paddle.left = screen_width - paddle.width
        
        #공과 벽돌 충돌 처리
            for brick in bricks:
                if ball.colliderect(brick):
                    bricks.remove(brick)                                                                    #해당 벽돌 제거
                    ball_dy = -ball_dy                                                                      #공 반사
                    score += 1                                                                              #점수 1점 증가


        #공과 패들 충돌처리

        if ball.colliderect(paddle):
            ball_dy = -ball_dy                                                                          #공이 패들과 부딪히면 위로 반사
            hit_sound.play()  # 🔊 패들과 충돌 시 효과음
            if ball.centerx <= paddle.left or ball.centerx > paddle.right:                              #만약 공이 패들의 가장자리에 닿았으면 X축 방향도 반사
                ball_dx = ball_dx * -1 


        #레벨 클리어 조건 (남은 벽돌이 없으면 클리어)
            if len(bricks) == 0:
                Level += 1
                Life += 1
                ball_dx = float(ball_dx * 1.15) if ball_dx > 0 else float(ball_dx * 1.15)
                ball_dy = float(ball_dy * 1.15) if ball_dy > 0 else float(ball_dy * 1.15)
                
                # 다음 레벨로 가기 전에 선택 화면
                pygame.display.update()
                if not show_level_cleared_screen(Level):
                    return  # 사용자가 종료를 선택하면 게임 종료

                bricks = []
                COLUMN_COUNT = 8
                ROW_COUNT = min(3 + Level, 6)

                for column_index in range(COLUMN_COUNT):
                    for row_index in range(ROW_COUNT):
                        brick = pygame.Rect(
                            column_index * (60 + 10) + 35,
                            row_index * (16 + 5) + 80, 60, 16
                        )
                        bricks.append(brick)

                ball.left = screen_width // 2 - ball.width // 2
                ball.top = screen_height // 2 - ball.height // 2
                ball_dy = -abs(ball_dy)

                if Level > 3:
                    game_over = SUCCESS


        #화면 그리기
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick, border_radius=2)

        if game_over == 0:
            pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2)

        pygame.draw.rect(screen, BLUE, paddle, border_radius=5)


        score_image = small_font.render('Point {}'.format(score), True, YELLOW)
        screen.blit(score_image, (10, 10))

        Life_image = small_font.render('Life {}'.format(Life), True, RED)
        screen.blit(Life_image, Life_image.get_rect(right=screen_width - 10, top=10))

        level_image = small_font.render('Level {}'.format(Level), True, YELLOW)
        screen.blit(level_image, (10, 40))

        if game_over == FAILURE:
            failure_image = large_font.render('Game Over', True, RED)
            screen.blit(failure_image, failure_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        if game_over == SUCCESS:
            success_image = large_font.render('You win!', True, BLUE)
            screen.blit(success_image, success_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))


        if paused:
            pause_text = large_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        pygame.display.update()

def show_level_cleared_screen(level):
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    message = large_font.render(f"Level {level - 1} Cleared!", True, WHITE)
    continue_text = small_font.render("Press C to Continue", True, GREEN)
    quit_text = small_font.render("Press Q to Quit", True, RED)

    screen.blit(message, message.get_rect(center=(screen_width // 2, screen_height // 2 - 60)))
    screen.blit(continue_text, continue_text.get_rect(center=(screen_width // 2, screen_height // 2)))
    screen.blit(quit_text, quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50)))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return False

def main():
    while True:
        result = show_start_screen()
        if result is None:
            break  # 게임 종료
        selected_game, sound_on = result
        pygame.mixer.music.set_volume(INITIAL_VOLUME if sound_on else 0.0)

        if selected_game == 'block':
            runBrickGame(sound_on)
        elif selected_game == 'snake':
            runSnakeGame()
        # 스네이크 게임 후 화면 크기 원래대로 복원
            global screen
            screen = pygame.display.set_mode((screen_width, screen_height))



main()
pygame.quit()