import pygame
from sys import exit
import config
import components
import population
import buttercup

pygame.init()
clock = pygame.time.Clock()
population = population.Population(50)
butter = buttercup.Buttercup()
pygame.display.set_caption("Flappy Bird")
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
butter.alive = False
r = 0
score = 0
score1=0

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		config.window.blit(self.image, (self.rect.x, self.rect.y))

		return action
    



def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                butter.flap_wings()



def main():
    # Load background image
    background_image = pygame.image.load("./image/bg2.png")
    button_img=pygame.image.load("./image/restart.png")
    pipes_spawn_time = 10
    global score, r, score1, game_over
    button = Button(config.win_width // 2 -70, config.win_height //2 -20 , button_img)

    # Initialize game over delay
    game_over_delay = 20

    while True:
        clock.tick(120)
        quit_game()

        # Draw background image
        config.window.blit(background_image, (0, 0))

        # Spawn Ground
        config.ground.draw(config.window)

        if not game_over:
            # Spawn Pipes
            if pipes_spawn_time <= 0:
                generate_pipes()
                pipes_spawn_time = 300
            pipes_spawn_time -= 1

            for p in config.pipes:
                p.draw(config.window)
                p.update()
                if p.off_screen:
                    config.pipes.remove(p)
                else:
                    if p.x + components.Pipes.width < population.players[0].x and not p.score_counted and not population.extinct():
                        score1 += 1
                        p.score_counted = True

                    if p.x + components.Pipes.width < butter.rect.x and not p.score_counted1 and butter.alive:
                        score += 1
                        p.score_counted1 = True

            # Display scores
            font = pygame.font.Font(None, 36)
            score_surface = font.render(f"Buttercup Score: {score}", True, (255, 255, 255))
            config.window.blit(score_surface, (10, 10))
            score_surface1 = font.render(f"Mojojojo Score: {score1}", True, (255, 255, 255))
            config.window.blit(score_surface1, (280, 10))

            # Check condition to update and draw Buttercup

            # Update population and increment r
            if not population.extinct() or butter.alive:
                population.update_live_players()
            else:
                score1 = 0
                score = 0
                if r < 2:
                    config.pipes.clear()
                    population.natural_selection()
                    r += 1  # Increment r after the population is reset

            if r >= 2:
                butter.alive = True
                butter.update(config.ground)
                butter.draw(config.window)

        else:
            # Draw the button and restart the game if it's clicked
            if button.draw():
                print("Button Clicked")
                config.pipes.clear()
                butter.restart()
                population.natural_selection()
                game_over_delay = 20
                score1 = 0
                score = 0
                game_over = False  # Reset game_over flag to allow the game to restart

        # Decrement game over delay and check for game over condition
        if not butter.alive and r>=2:
            game_over_delay -= 1
            if game_over_delay <= 0:
                game_over = True

        pygame.display.flip()

main()
