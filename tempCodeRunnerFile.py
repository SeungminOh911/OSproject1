import sys
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_SPACE

from implements import Basic, Block, WallBlock, Paddle, Ball, Item
import config


pygame.init()
pygame.key.set_repeat(3, 3)
surface = pygame.display.set_mode(config.display_dimension)

fps_clock = pygame.time.Clock()

paddle = Paddle()
ball1 = Ball()
BLOCKS = []
ITEMS = []
BALLS = [ball1]
life = config.life
start = False


# 블록 생성 함수
def create_blocks():
    for i in range(config.num_blocks[0]):
        for j in range(config.num_blocks[1]):
            x = config.margin[0] + i * (config.block_size[0] + config.spacing[0])
            y = (
                config.margin[1]
                + config.scoreboard_height
                + j * (config.block_size[1] + config.spacing[1])
            )

            # 두 번째 줄(j == 1)은 회색 벽 블록 생성
            if j == 1:
                block = WallBlock((x, y))
            else:
                color_index = j % len(config.colors)
                color = config.colors[color_index]
                block = Block(color, (x, y))
            BLOCKS.append(block)


# 게임 상태 업데이트
def tick():
    global life, BLOCKS, ITEMS, BALLS, paddle, ball1, start
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:  
                start = True
            paddle.move_paddle(event)

    for ball in BALLS:
        if start:
            ball.move()
        else:
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top

        ball.collide_block(BLOCKS, ITEMS)
        ball.collide_paddle(paddle)
        ball.hit_wall()
        
        if not ball.alive():
            BALLS.remove(ball)

    # 아이템 이동 및 패들과 충돌 체크
    for item in ITEMS[:]:
        item.move()
        if item.rect.colliderect(paddle.rect):
            ITEMS.remove(item)  # 아이템 제거 (추후 효과 구현 가능)
        elif item.rect.top >= config.display_dimension[1]:
            ITEMS.remove(item)  # 바닥에 닿으면 제거


# 메인 게임 루프
def main():
    global life, BLOCKS, ITEMS, BALLS, paddle, ball1, start
    my_font = pygame.font.SysFont(None, 50)
    mess_clear = my_font.render("Cleared!", True, config.colors[2])
    mess_over = my_font.render("Game Over!", True, config.colors[2])
    create_blocks()

    while True:
        tick()
        surface.fill((0, 0, 0))
        paddle.draw(surface)

        # 블록 그리기
        for block in BLOCKS:
            block.draw(surface)

        # 아이템 그리기
        for item in ITEMS:
            item.draw(surface)

        # 점수 및 생명 상태 표시
        cur_score = config.num_blocks[0] * config.num_blocks[1] - len(
            [block for block in BLOCKS if isinstance(block, Block)]
        )

        score_txt = my_font.render(f"Score : {cur_score * 10}", True, config.colors[2])
        life_font = my_font.render(f"Life: {life}", True, config.colors[0])

        surface.blit(score_txt, config.score_pos)
        surface.blit(life_font, config.life_pos)

        if len(BALLS) == 0:
            if life > 1:
                life -= 1
                ball1 = Ball()
                BALLS = [ball1]
                start = False
            else:
                surface.blit(mess_over, (200, 300))
        elif all(not block.alive for block in BLOCKS if isinstance(block, Block)):
            surface.blit(mess_clear, (200, 400))
        else:
            for ball in BALLS:
                if start:
                    ball.move()
                ball.draw(surface)

        pygame.display.update()
        fps_clock.tick(config.fps)


if __name__ == "__main__":
    main()
