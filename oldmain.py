def run_game():
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

    surface = pygame.display.set_mode(SIZE)

    timer = Timer(120, 25)

    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0)
    player1 = Player(200, SCREEN_HEIGHT // 2, BLUE, PLAYER1_CONTROLS)
    player2 = Player(600, SCREEN_HEIGHT // 2, RED, PLAYER2_CONTROLS)
    players = [player1, player2]

    player1_score = 0
    player2_score = 0

    ball_held = False

    while 1:
        draw_field(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        # Draw & Update players, throw ball
        for player in players:
            player.draw(surface)
            ball_thrown = player.update(keys)
            if ball_thrown:
                ball = player.get_thrown_ball()
                ball_held = False

        # Draw & Update ball, catch ball
        if not ball_held:
            ball.draw(surface)
            ball.update()

            for player in players:
                if circle_collision(player.get_ball_pos(), ball.get_pos(), PLAYER_RADIUS, BALL_RADIUS):
                    player.has_ball = True
                    ball_held = True
                    ball = None
                    break

        #Check Goal1
        if ball is not None and ball.get_pos()[0] < 5 and ball.get_pos()[1] >= GOAL_LOW_Y + BALL_RADIUS \
                and ball.get_pos()[1] <= GOAL_HIGH_Y - BALL_RADIUS:
            player2_score += 1
            timer.freeze(1.5)
            ball = Ball(400, 300, 0, 0)
            for player in players:
                player.reset()

        # Check Goal2
        if ball is not None and ball.get_pos()[0] > SCREEN_WIDTH - 5 and ball.get_pos()[1] >= GOAL_LOW_Y + BALL_RADIUS \
                and ball.get_pos()[1] <= GOAL_HIGH_Y - BALL_RADIUS:
            player1_score += 1
            timer.freeze(1.5)
            ball = Ball(400, 300, 0, 0)
            for player in players:
                player.reset()

        # Check goal zones
        goal1_check = circle_collision(player2.get_pos(), (0, SCREEN_HEIGHT // 2), PLAYER_RADIUS,
                                       GOAL_ZONE_RADIUS)
        if goal1_check:
            player2.bounce(goal1_check, friction=GOAL_BOUNCE_FRICTION)
        goal2_check = circle_collision(player1.get_pos(), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), PLAYER_RADIUS,
                                       GOAL_ZONE_RADIUS)
        if goal2_check:
            player1.bounce(goal2_check, friction=GOAL_BOUNCE_FRICTION)

        # Check players colliding
        player_collision = circle_collision(player1.get_pos(), player2.get_pos(), PLAYER_RADIUS, PLAYER_RADIUS)
        if player_collision:
            new_speed = player1.get_speed() + player2.get_speed() / 2
            if player1.has_ball:
                ball_held = False
                player1.has_ball = False
                ball = player1.get_thrown_ball()
            if player2.has_ball:
                ball_held = False
                player2.has_ball = False
                ball = player2.get_thrown_ball()
            player1.bounce(player_collision, speed=new_speed)
            player2.bounce(player_collision + pi, speed=new_speed)

        # Check players colliding with ball
        if not ball_held:
            for player in players:
                player_ball_collision = circle_collision(player.get_pos(), ball.get_pos(), PLAYER_RADIUS, BALL_RADIUS)
                if player_ball_collision:
                    new_speed = player.get_speed() + ball.get_speed() / 2
                    player.bounce(player_ball_collision, speed=new_speed)
                    ball.bounce(player_ball_collision + pi, speed=new_speed)

        timer.tick()

        if not timer.is_frozen():
            for player in players:
                player.unfreeze()

        if timer.is_finished():
            break

        draw_score(surface, player1_score, player2_score, timer, font)

        pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()