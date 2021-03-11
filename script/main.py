import pygame

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

FPS = 60

Beispielbild = pygame.image.load('Assets\\enemys\\beispiel.jpg')

Beispielbild = pygame.transform.scale(Beispielbild,(100,80))
Beispielbild2 = pygame.image.load('Assets\\enemys\\beispiel.jpg')

Beispielbild2 = pygame.transform.scale(Beispielbild2,(100,80))

def draw_window(pic,pic2, bullets):
    WINDOW.fill((255, 255, 255))
    WINDOW.blit(Beispielbild, (pic.x,pic.y))
    WINDOW.blit(Beispielbild2, (pic2.x, pic2.y))
    for b in bullets:
        pygame.draw.rect(WINDOW,(255,0,0),b)
    pygame.display.update()

def movement(bild,keys_pressed):
    if keys_pressed[pygame.K_LEFT]:
        bild.x -= 1
    if keys_pressed[pygame.K_RIGHT]:
        bild.x += 1
    if keys_pressed[pygame.K_DOWN]:
        bild.y += 1
    if keys_pressed[pygame.K_UP]:
        bild.y -= 1


def handle_bullets(bullets, bild2):
    for b in bullets:
        b.x +=5
        if bild2.colliderect(b):
            print("TREEEEFFFEEER")
            bullets.remove(b)
        elif b.x > WIDTH:
            bullets.remove(b)


def main_game_loop():
    
    bullets = []
    
    bild = pygame.Rect(50,50,100,80)

    bild2 = pygame.Rect(500, 50, 100, 80)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(bild.x + bild.width, bild.y + bild.height//2, 10, 5)
                    bullets.append(bullet)

        movement(bild,pygame.key.get_pressed())
        handle_bullets(bullets,bild2)
        draw_window(bild,bild2, bullets)
    pygame.quit()


if __name__ == "__main__":
    main_game_loop()
