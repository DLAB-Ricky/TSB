import pygame, sys
import random
from monster import Monster
from pygame.locals import *

pygame.init()
# pygame.mixer.init()

score = 0

# 객체 속도
MONSTER_SPEED = 15

# 객체 생성 이벤트 정의
NEW_OBJECT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_OBJECT_EVENT, 1000)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 화면 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("classic_forest.ogg")

# 배경음악 로드
bgm = pygame.mixer.Sound("classic_forest.ogg")  # 파일 경로에 맞게 수정

# 배경음악 재생 (반복 재생)
bgm.play()  # -1은 무한 반복, 1은 한 번만 재생

# 캐릭터 데이터 관리
knight = {
    'rect': pygame.Rect(0, height - 265, 60, 100),
    'image_right': pygame.transform.scale(pygame.image.load('images/knight.png'), (60, 100)),
    'image_left': None,
    'vl': 20,
    'is_jumping': False,
    'jump_step': 4
}
knight['image_left'] = pygame.transform.flip(knight['image_right'], True, False)
knight['image'] = knight['image_right']

# 일반 몬스터 생성
일반몬스터 = Monster('images/일반몬.png', 'images/bullet1.png', 10, 50, (width - 100, height - 300), (100, 100))
monsterlist = [일반몬스터]

# 배경 이미지 설정
bg_image = pygame.image.load('images/lv-1.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))
backX, backX2 = 0, width  # 배경 두 장을 이어 붙여 스크롤 효과 구현

def game_over():
    screen.fill((0, 0, 0))  # 화면을 검은색으로 채우기
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # 빨간색으로 텍스트 렌더링
    game_over_score = font.render(f"SCORE: {score}", True, (255,255,255)) #점수
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2))
    screen.blit(game_over_score, (width // 2 - game_over_text.get_width() // 2, height // 3))
    pygame.display.update()  # 화면 업데이트
    pygame.time.delay(3000)  # 3초간 대기
    pygame.quit()
    sys.exit()

# 메인 게임 루프
while True:
    pygame.time.delay(40)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == NEW_OBJECT_EVENT:
            # 2초마다 새로운 객체 생성
            position = (800, random.randint(170, 350))
            new_object = Monster('images/일반몬.png', 'images/bullet1.png', 10, 50, position, (100, 100))
            monsterlist.append(new_object)

    # 키 입력 처리
    key_input = pygame.key.get_pressed()
    if key_input[K_LEFT] and knight['rect'].left > 0:
        knight['rect'].left -= knight['vl']
        knight['image'] = knight['image_left']

    if key_input[K_RIGHT] and knight['rect'].right < width:
        if knight['rect'].left <= width * 0.5 - 30:
            knight['rect'].right += knight['vl']
        else:
            backX -= (knight['vl'] + MONSTER_SPEED)
            backX2 -= (knight['vl'] + MONSTER_SPEED)
        knight['image'] = knight['image_right']

    # A키와 충돌 감지 처리
    if key_input[K_a]:
        for monster in monsterlist[:]:  # 리스트 복사본을 순회하며 제거
            if knight['rect'].colliderect(monster.rect):  # 충돌 감지
                monsterlist.remove(monster)  # 충돌한 몬스터 제거
                score += 1

    # 점프 처리
    if not knight['is_jumping']:
        if key_input[K_SPACE]:
            knight['is_jumping'] = True
    else:
        if knight['jump_step'] >= -4:
            knight['rect'].top -= knight['jump_step'] * abs(knight['jump_step']) * 5
            knight['jump_step'] -= 1
        else:
            knight['is_jumping'] = False
            knight['jump_step'] = 4

    # 몬스터 이동 및 게임 오버 조건 체크
    for monster in monsterlist[:]:  # 리스트 복사본 순회
        monster.move_left(MONSTER_SPEED)
        if monster.rect.right <= 0:  # 몬스터가 화면 왼쪽으로 나가면 게임 오버
            game_over()

    # 배경 위치 조정 (스크롤 효과)
    if backX < -width:
        backX *= -1
    if backX2 < -width:
        backX2 *= -1

    # 배경 그리기 (화면 지우기)
    screen.blit(bg_image, (backX, 0))
    screen.blit(bg_image, (backX2, 0))

    # 몬스터 그리기
    for monster in monsterlist:
        monster.draw(screen)

    # 캐릭터 그리기
    screen.blit(knight['image'], knight['rect'].topleft)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.mixer.music.stop()
    pygame.display.update()