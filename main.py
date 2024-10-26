import pygame, sys
from monster import Monster
from pygame.locals import *

pygame.init()

# 화면 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# 캐릭터 데이터 관리
knight = {
    'rect': pygame.Rect(0, height - 165, 60, 100),
    'image_right': pygame.transform.scale(pygame.image.load('images/knight.png'), (60, 100)),
    'image_left': None,
    'vl': 5,
    'is_jumping': False,
    'jump_step': 4
}
knight['image_left'] = pygame.transform.flip(knight['image_right'], True, False)
knight['image'] = knight['image_right']



일반몬스터 = Monster('images/일반몬.png', 'images/bullet1.png', 10, 50, (width - 100, height - 200), (100,100))
monsterlist = [일반몬스터]
# 배경 이미지 설정
bg_image = pygame.image.load('images/tsb bg1.jpeg')
bg_image = pygame.transform.scale(bg_image, (width, height))
backX, backX2 = 0, width  # 배경 두 장을 이어 붙여 스크롤 효과 구현

# 게임 루프
while True:
    pygame.time.delay(40)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력 처리
    key_input = pygame.key.get_pressed()
    if key_input[K_LEFT] and knight['rect'].left > 0:
        knight['rect'].left -= knight['vl']
        knight['image'] = knight['image_left']

    if key_input[K_RIGHT] and knight['rect'].right < width:
        if knight['rect'].left <= width * 0.5 -30:
            knight['rect'].right += knight['vl']
        else:
            backX -= knight['vl']
            backX2 -= knight['vl']
        knight['image'] = knight['image_right']


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

    # 몬스터 리젠
    for monster in monsterlist:
        monster.move_left(3)

    # 배경 위치 조정 (스크롤 효과)
    if backX < -width:
        backX *= -1
    if backX2 < -width:
        backX2 *= -1
    if backX > 0:
        backX -= width
        backX2 -= width

    # 배경 그리기 (화면 지우기)
    screen.blit(bg_image, (backX, 0))
    screen.blit(bg_image, (backX2, 0))

    for monster in monsterlist:
        monster.draw(screen)

    # 캐릭터 그리기
    screen.blit(knight['image'], knight['rect'].topleft)

    # 화면 업데이트
    pygame.display.update()