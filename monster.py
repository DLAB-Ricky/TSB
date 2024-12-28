import pygame

class Monster:
    def __init__(self, image_path, _bullet_imagepath, attack_power, health, position, size):
        # 몬스터 이미지 로드
        self.image = pygame.transform.scale(pygame.image.load(image_path), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        # 몬스터 총알 이미지 로드
        self.bullet_image = pygame.image.load(_bullet_imagepath)

        # 몬스터의 속성 설정
        self.attack_power = attack_power
        self.health = health
        self.position = position  # 현재 위치
        self.size = size # 몬스터 크기
        self.bullets = []  # 몬스터가 발사한 총알들

    def draw(self, screen):
        """스크린에 몬스터를 그림"""
        screen.blit(self.image, self.rect)

    def move_left(self, velocity):
        self.rect.left -= velocity

    def move_right(self, velocity):
        self.rect.right += velocity

    def take_damage(self, damage):
        """데미지를 받아 체력을 줄임"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0  # 체력은 0 이하로 내려가지 않음

    def attack(self):
        """공격 시 총알 발사"""
        bullet_rect = self.bullet_image.get_rect(center=self.rect.center)
        self.bullets.append(bullet_rect)

    def update_bullets(self, speed):
        """총알 위치 업데이트"""
        for bullet in self.bullets:
            bullet.x += speed  # 원하는 방향과 속도 설정
        self.bullets = [bullet for bullet in self.bullets if bullet.x < 800]  # 예시로 화면을 벗어나면 삭제

    def is_dead(self):
        """몬스터가 죽었는지 여부 반환"""
        return self.health <= 0