import pygame, sys
from pygame.locals import *

pygame.init()

# 화면 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# 캐릭터 데이터 관리
knight = {
    'rect': pygame.Rect(0, height - 165, 60, 100),
    'image_right': pygame.transform.scale(pygame.image.load('pixel_k-removebg-preview.png'), (60,100)),
    'image_left': None,
    'vl': 5,
    'is_jumping': False,
    'jump_step': 4
}
knight['image_left'] = pygame.transform.flip(knight['image_right'], True, False)
knight['image'] = knight['image_right']
# 배경 이미지 설정
bg_image = pygame.image.load('tsb bg1.jpeg')
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
        backX += knight['vl']
        backX2 += knight['vl']
        knight['rect'].left -= knight['vl']
        knight['image'] = knight['image_left']

    if key_input[K_RIGHT] and knight['rect'].right < width:
        backX -= knight['vl']
        backX2 -= knight['vl']
        knight['rect'].right += knight['vl']
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

    # 배경 위치 조정 (스크롤 효과)
    if backX < -width:
        backX = width
    if backX2 < -width:
        backX2 = width
    if backX > 0:
        backX = -width
    if backX2 > 0:
        backX2 = -width

    # 배경 그리기 (화면 지우기)
    screen.blit(bg_image, (backX, 0))
    screen.blit(bg_image, (backX2, 0))

    # 캐릭터 그리기
    screen.blit(knight['image'], knight['rect'].topleft)

    # 화면 업데이트
    pygame.display.update()