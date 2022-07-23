import pygame


# access the graphics related functions
class Graphics:
    # Initialize pygame

    # Initialize the window
    def Window(title, wh: tuple):
        pygame.display.set_mode(wh)
        pygame.display.set_caption(title)

    # main function for graphics class
    def __main__():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
