import pygame, sys
from constants import *
from ball import Ball
from player import Player
from math import sqrt, pi, atan
from timer import Timer
from team import Team


def circle_collision(pos1, pos2, r1, r2):
    x_diff = pos1[0] - pos2[0]
    y_diff = pos1[1] - pos2[1]
    dist = sqrt(x_diff ** 2 + y_diff ** 2)
    has_collided = dist < (r1 + r2)
    diff_angle = atan(-1 * y_diff / x_diff) if x_diff != 0 else (pi / -2 if y_diff > 0 else pi / 2)
    if x_diff < 0:
        diff_angle += pi
    if has_collided:
        return diff_angle + (0.00001 if diff_angle == 0 else 0)
    else:
        return False


def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def check_for_scores(ball, team1, team2):
    # Check Goal1
    if ball is not None and ball.get_pos()[0] < 5 \
            and abs(ball.get_pos()[1] - SCREEN_HEIGHT // 2) <= GOAL_WIDTH // 2 - BALL_RADIUS:
        team2.inc_score()
        return True

    # Check Goal2
    if ball is not None and ball.get_pos()[0] > SCREEN_WIDTH - 5 \
            and abs(ball.get_pos()[1] - SCREEN_HEIGHT // 2) <= GOAL_WIDTH // 2 - BALL_RADIUS:
        team1.inc_score()
        return True

    return False


def draw_score(screen, player1_score, player2_score, timer, font):
    text = '{} - {} {}'.format(player1_score, player2_score, timer)
    rendered_text = font.render(text, False, WHITE)
    rect = rendered_text.get_bounding_rect()
    screen.blit(rendered_text, ((SCREEN_WIDTH - rect.width) // 2, 0))


def draw_field(surface):
    surface.fill(GRASS_GREEN)
    pygame.draw.circle(surface, BLACK, (0, SCREEN_HEIGHT // 2), GOAL_ZONE_RADIUS, BORDER_WIDTH)
    pygame.draw.circle(surface, BLACK, (SCREEN_WIDTH, SCREEN_HEIGHT // 2), GOAL_ZONE_RADIUS, BORDER_WIDTH)

    pygame.draw.circle(surface, WHITE, (0, SCREEN_HEIGHT // 2), GOAL_ZONE_RADIUS - BORDER_WIDTH)
    pygame.draw.circle(surface, WHITE, (SCREEN_WIDTH, SCREEN_HEIGHT // 2), GOAL_ZONE_RADIUS - BORDER_WIDTH)

    pygame.draw.line(surface, BLACK, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), BORDER_WIDTH)

    pygame.draw.circle(surface, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), CENTER_ZONE_RADIUS, BORDER_WIDTH)
    pygame.draw.circle(surface, GRASS_GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), CENTER_ZONE_RADIUS - BORDER_WIDTH)

    pygame.draw.lines(surface, BLACK, False, GOAL1_COORDS, BORDER_WIDTH)
    pygame.draw.lines(surface, BLACK, False, GOAL2_COORDS, BORDER_WIDTH)


def run():
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

    surface = pygame.display.set_mode(SIZE)

    timer = Timer(300, 25)

    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0)

    team1 = Team([Player(200, SCREEN_HEIGHT // 2, BLUE, PLAYER1_CONTROLS)])
    team2 = Team([Player(600, SCREEN_HEIGHT // 2, RED, PLAYER2_CONTROLS)])
    players = team1.players + team2.players

    ball_held = False

    while not timer.is_finished():
        check_quit()

        draw_field(surface)
        draw_score(surface, team1.score, team2.score, timer, font)
        for player in players:
            player.draw(surface)

        timer.tick()

        if timer.is_frozen():
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        for i in range(len(players)):
            if players[i].update(keys):
                ball = players[i].get_thrown_ball()
                ball_held = False
            for j in range(i + 1, len(players)):
                if players[i] is not players[j]:
                    players[i].check_collision(players[j])


        for player1 in team1.players:
            goal2_check = circle_collision(player1.get_pos(), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), PLAYER_RADIUS,
                                           GOAL_ZONE_RADIUS)
            if goal2_check:
                player1.bounce(goal2_check, friction=GOAL_BOUNCE_FRICTION)

        for player2 in team2.players:
            goal1_check = circle_collision(player2.get_pos(), (0, SCREEN_HEIGHT // 2), PLAYER_RADIUS,
                                           GOAL_ZONE_RADIUS)
            if goal1_check:
                player2.bounce(goal1_check, friction=GOAL_BOUNCE_FRICTION)

        if not ball_held:
            ball.draw(surface)
            ball.update()
            for player in players:
                if player.can_catch_ball() and \
                        circle_collision(player.get_ball_pos(), ball.get_pos(), PLAYER_RADIUS, BALL_RADIUS):
                    player.has_ball = True
                    ball_held = True
                    ball = None
                    break
                player.check_collision(ball)
            if check_for_scores(ball, team1, team2):
                timer.freeze(1.5)
                ball = Ball(400, 300, 0, 0)
                for player in players:
                    player.reset()


        pygame.display.flip()

    while 1:
        check_quit()

if __name__ == '__main__':
    run()