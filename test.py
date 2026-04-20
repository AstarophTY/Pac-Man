#!/usr/bin/env python3
"""
PAC-MAN - Version Arcade Rétro
Créé avec Raylib
Contrôles: Flèches directionnelles
"""

import random
from pyray import *
from raylib import Color

# Constantes du jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 25
GRID_WIDTH = 28
GRID_HEIGHT = 22

# Couleurs personnalisées arcade
COLOR_BG = Color(10, 10, 30, 255)
COLOR_WALL = Color(33, 33, 255, 255)
COLOR_WALL_GLOW = Color(66, 66, 255, 120)
COLOR_DOT = Color(255, 184, 174, 255)
COLOR_POWER_PELLET = Color(255, 255, 100, 255)
COLOR_PACMAN = Color(255, 255, 0, 255)
COLOR_GHOST_BLINKY = Color(255, 0, 0, 255)
COLOR_GHOST_PINKY = Color(255, 184, 255, 255)
COLOR_GHOST_INKY = Color(0, 255, 255, 255)
COLOR_GHOST_CLYDE = Color(255, 184, 82, 255)
COLOR_GHOST_SCARED = Color(33, 33, 255, 255)
COLOR_TEXT = Color(255, 255, 255, 255)
COLOR_SCORE_GLOW = Color(255, 255, 0, 200)

# Labyrinthe classique Pac-Man (1 = mur, 0 = vide, 2 = dot, 3 = power pellet)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Directions
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

class Pacman:
    def __init__(self):
        self.x = 14
        self.y = 18
        self.direction = DIR_LEFT
        self.next_direction = DIR_LEFT
        self.mouth_angle = 0
        self.mouth_opening = True
        self.animation_speed = 10
        
    def update(self, maze):
        # Animation de la bouche
        if self.mouth_opening:
            self.mouth_angle += self.animation_speed
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= self.animation_speed
            if self.mouth_angle <= 0:
                self.mouth_opening = True
        
        # Essayer de changer de direction
        new_x = self.x + self.next_direction[0]
        new_y = self.y + self.next_direction[1]
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if maze[new_y][new_x] != 1:
                self.direction = self.next_direction
        
        # Déplacement
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        # Téléportation gauche-droite
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
            
        # Vérifier collision
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if maze[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y
    
    def draw(self, offset_x, offset_y):
        center_x = offset_x + self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = offset_y + self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Déterminer l'angle de rotation selon la direction
        rotation = 0
        if self.direction == DIR_RIGHT:
            rotation = 0
        elif self.direction == DIR_LEFT:
            rotation = 180
        elif self.direction == DIR_UP:
            rotation = 270
        elif self.direction == DIR_DOWN:
            rotation = 90
        
        # Dessiner Pac-Man avec effet de lueur
        draw_circle(center_x, center_y, radius + 3, Color(255, 255, 0, 50))
        draw_circle_sector(
            Vector2(center_x, center_y),
            radius,
            rotation + self.mouth_angle,
            rotation + 360 - self.mouth_angle,
            36,
            COLOR_PACMAN
        )

class Ghost:
    def __init__(self, x, y, color, name):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.direction = DIR_UP
        self.scared = False
        self.scared_timer = 0
        
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.scared = False
        self.scared_timer = 0
        
    def update(self, maze, pacman_x, pacman_y):
        if self.scared:
            self.scared_timer -= 1
            if self.scared_timer <= 0:
                self.scared = False
        
        # IA simple : directions possibles
        possible_dirs = []
        for d in [DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT]:
            new_x = self.x + d[0]
            new_y = self.y + d[1]
            
            # Téléportation
            if new_x < 0:
                new_x = GRID_WIDTH - 1
            elif new_x >= GRID_WIDTH:
                new_x = 0
            
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if maze[new_y][new_x] != 1:
                    possible_dirs.append(d)
        
        if possible_dirs:
            if self.scared:
                # Fuir Pac-Man
                self.direction = random.choice(possible_dirs)
            else:
                # Chasser Pac-Man (IA basique)
                best_dir = possible_dirs[0]
                best_dist = abs(self.x + best_dir[0] - pacman_x) + abs(self.y + best_dir[1] - pacman_y)
                
                for d in possible_dirs:
                    dist = abs(self.x + d[0] - pacman_x) + abs(self.y + d[1] - pacman_y)
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d
                
                self.direction = best_dir
        
        # Déplacement
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        # Téléportation
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if maze[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y
    
    def draw(self, offset_x, offset_y):
        center_x = offset_x + self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = offset_y + self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        color = COLOR_GHOST_SCARED if self.scared else self.color
        
        # Corps du fantôme avec effet de lueur
        draw_circle(center_x, center_y, radius + 3, Color(color.r, color.g, color.b, 50))
        draw_circle(center_x, center_y - 3, radius, color)
        
        # Bas ondulé du fantôme
        for i in range(5):
            x = center_x - radius + i * (radius * 2 // 4)
            y = center_y + radius // 2
            draw_circle(x, y, radius // 3, color)
        
        # Yeux
        eye_color = WHITE
        pupil_color = COLOR_GHOST_SCARED if self.scared else Color(33, 33, 255, 255)
        
        draw_circle(center_x - 5, center_y - 5, 4, eye_color)
        draw_circle(center_x + 5, center_y - 5, 4, eye_color)
        draw_circle(center_x - 5, center_y - 5, 2, pupil_color)
        draw_circle(center_x + 5, center_y - 5, 2, pupil_color)

class Game:
    def __init__(self):
        self.maze = [row[:] for row in MAZE]
        self.pacman = Pacman()
        self.ghosts = [
            Ghost(13, 11, COLOR_GHOST_BLINKY, "Blinky"),
            Ghost(14, 11, COLOR_GHOST_PINKY, "Pinky"),
            Ghost(13, 12, COLOR_GHOST_INKY, "Inky"),
            Ghost(14, 12, COLOR_GHOST_CLYDE, "Clyde"),
        ]
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.win = False
        self.move_timer = 0
        self.move_delay = 3  # Plus rapide = plus petit
        self.dots_remaining = self.count_dots()
        self.glow_pulse = 0
        
    def count_dots(self):
        count = 0
        for row in self.maze:
            for cell in row:
                if cell in [2, 3]:
                    count += 1
        return count
    
    def reset_positions(self):
        self.pacman = Pacman()
        for ghost in self.ghosts:
            ghost.reset()
    
    def update(self):
        if self.game_over or self.win:
            return
        
        self.glow_pulse = (self.glow_pulse + 0.1) % 6.28
        
        # Input
        if is_key_down(KEY_UP):
            self.pacman.next_direction = DIR_UP
        elif is_key_down(KEY_DOWN):
            self.pacman.next_direction = DIR_DOWN
        elif is_key_down(KEY_LEFT):
            self.pacman.next_direction = DIR_LEFT
        elif is_key_down(KEY_RIGHT):
            self.pacman.next_direction = DIR_RIGHT
        
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            
            # Mettre à jour Pac-Man
            self.pacman.update(self.maze)
            
            # Vérifier collecte de dots
            cell = self.maze[self.pacman.y][self.pacman.x]
            if cell == 2:
                self.maze[self.pacman.y][self.pacman.x] = 0
                self.score += 10
                self.dots_remaining -= 1
            elif cell == 3:
                self.maze[self.pacman.y][self.pacman.x] = 0
                self.score += 50
                self.dots_remaining -= 1
                # Effrayer les fantômes
                for ghost in self.ghosts:
                    ghost.scared = True
                    ghost.scared_timer = 100
            
            # Vérifier victoire
            if self.dots_remaining == 0:
                self.win = True
            
            # Mettre à jour fantômes
            for ghost in self.ghosts:
                ghost.update(self.maze, self.pacman.x, self.pacman.y)
                
                # Vérifier collision avec Pac-Man
                if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                    if ghost.scared:
                        self.score += 200
                        ghost.reset()
                    else:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            self.reset_positions()
    
    def draw(self):
        clear_background(COLOR_BG)
        
        # Calculer offset pour centrer
        offset_x = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
        offset_y = 80
        
        # Dessiner le titre avec effet néon
        title = "PAC-MAN"
        title_size = 50
        title_width = measure_text(title, title_size)
        glow_offset = int(abs(3 * (1 + 0.5 * (self.glow_pulse % 3.14))))
        
        for i in range(3):
            draw_text(title, 
                     SCREEN_WIDTH // 2 - title_width // 2, 
                     15 + i, 
                     title_size, 
                     Color(255, 255, 0, 80 - i * 20))
        draw_text(title, 
                 SCREEN_WIDTH // 2 - title_width // 2, 
                 15, 
                 title_size, 
                 COLOR_PACMAN)
        
        # Dessiner le labyrinthe avec effet néon
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = self.maze[y][x]
                px = offset_x + x * CELL_SIZE
                py = offset_y + y * CELL_SIZE
                
                if cell == 1:
                    # Mur avec effet de lueur
                    draw_rectangle(px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4, COLOR_WALL_GLOW)
                    draw_rectangle(px + 3, py + 3, CELL_SIZE - 6, CELL_SIZE - 6, COLOR_WALL)
                    draw_rectangle_lines(px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4, COLOR_WALL_GLOW)
                elif cell == 2:
                    # Dot
                    draw_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 2, COLOR_DOT)
                elif cell == 3:
                    # Power pellet avec pulsation
                    pulse = abs(5 + 3 * (1 + 0.8 * (self.glow_pulse % 3.14)))
                    draw_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, pulse, 
                               Color(255, 255, 100, 100))
                    draw_circle(px + CELL_SIZE // 2, py + CELL_SIZE // 2, 5, COLOR_POWER_PELLET)
        
        # Dessiner les fantômes
        for ghost in self.ghosts:
            ghost.draw(offset_x, offset_y)
        
        # Dessiner Pac-Man
        self.pacman.draw(offset_x, offset_y)
        
        # HUD
        score_text = f"SCORE: {self.score}"
        draw_text(score_text, 20, SCREEN_HEIGHT - 40, 20, COLOR_TEXT)
        draw_text(score_text, 21, SCREEN_HEIGHT - 40, 20, COLOR_SCORE_GLOW)
        
        lives_text = f"VIES: {self.lives}"
        draw_text(lives_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40, 20, COLOR_TEXT)
        
        # Messages de fin
        if self.game_over:
            msg = "GAME OVER!"
            msg_width = measure_text(msg, 40)
            draw_rectangle(0, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH, 100, Color(0, 0, 0, 180))
            draw_text(msg, SCREEN_WIDTH // 2 - msg_width // 2, SCREEN_HEIGHT // 2 - 20, 40, RED)
            
            restart = "Appuyez sur R pour recommencer"
            restart_width = measure_text(restart, 20)
            draw_text(restart, SCREEN_WIDTH // 2 - restart_width // 2, SCREEN_HEIGHT // 2 + 30, 20, WHITE)
        
        if self.win:
            msg = "VICTOIRE!"
            msg_width = measure_text(msg, 40)
            draw_rectangle(0, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH, 100, Color(0, 0, 0, 180))
            draw_text(msg, SCREEN_WIDTH // 2 - msg_width // 2, SCREEN_HEIGHT // 2 - 20, 40, YELLOW)
            
            restart = "Appuyez sur R pour recommencer"
            restart_width = measure_text(restart, 20)
            draw_text(restart, SCREEN_WIDTH // 2 - restart_width // 2, SCREEN_HEIGHT // 2 + 30, 20, WHITE)

def main():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PAC-MAN - Arcade Rétro")
    set_target_fps(60)
    
    game = Game()
    
    while not window_should_close():
        # Restart
        if is_key_pressed(KEY_R):
            game = Game()
        
        game.update()
        
        begin_drawing()
        game.draw()
        end_drawing()
    
    close_window()

if __name__ == "__main__":
    main()