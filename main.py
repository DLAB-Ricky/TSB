import pygame, sys
from pygame.locals import*

pygame.init()

# 화면 크기 설정
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# 캐릭터 위치와 크기 설정
# TODO - r1이라는 변수명을 조금 더 의미있게 지어주세요. dictionary로 만들어서 체계적으로 관리해주세요 (spaceshooter 참고하면 됩니다.)
r1 = pygame.Rect(0, height - 130, 60, 100)

# 캐릭터 이미지 불러오기
right = pygame.image.load('pixel_k-removebg-preview.png')
right = pygame.transform.scale(right, (60, 100))
left = pygame.transform.flip(right, True, False)
knight = right

# 점프 상태 변수
isJump = False
jumpStep = 4

# 게임 루프
while True:
    pygame.time.delay(40)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력 처리
    keyInput = pygame.key.get_pressed()
    if keyInput[K_LEFT] and r1.left > 0:
        r1.left -= 10
        knight = left
    if keyInput[K_RIGHT] and r1.right < width:
        r1.left += 10
        knight = right

    if not isJump:  # 점프 중이 아닐 때만 점프 가능
        if keyInput[K_SPACE]:
            isJump = True
    else:  # 점프 중일 때
        if jumpStep >= -4:
            r1.top -= jumpStep * abs(jumpStep) * 5
            jumpStep -= 1
        else:
            isJump = False
            jumpStep = 4

    # 배경 그리기 (화면 지우기)
    screen.fill((0, 0, 0))  # 검은 배경

    # 캐릭터 그리기
    screen.blit(knight, r1)

    # 화면 업데이트
    pygame.display.update()