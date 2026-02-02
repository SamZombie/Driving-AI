import pygame
import math

class Car:
    def __init__(self, color=(255, 0, 0)):
        self.reset()
        self.max_forward_velocity = 5
        self.acceleration = 0.1
        self.color = color
        self.width = 40
        self.height = 20
        self.points = 0

    def reset(self):
        self.pos = (350, 100)
        self.angle = 0
        self.forward_velocity = 0
        self.points = 0
    
    def get_corners(self):
        corners = []
        for dx, dy in [(-self.width/2, -self.height/2), (self.width/2, -self.height/2),
                       (self.width/2, self.height/2), (-self.width/2, self.height/2)]:
            rotated_x = dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
            rotated_y = dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))
            corners.append((self.pos[0] + rotated_x, self.pos[1] + rotated_y))
        return corners

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.get_corners())

    def handle_input(self):
        keystates = pygame.key.get_pressed()
        if keystates[pygame.K_UP]:
            self.forward()
        else:
            self.stop()
        if keystates[pygame.K_LEFT]:
            self.turn_left()
        if keystates[pygame.K_RIGHT]:
            self.turn_right()

    def move(self, stop=False):
        dx = self.forward_velocity * math.cos(math.radians(self.angle))
        dy = self.forward_velocity * math.sin(math.radians(self.angle))
        if stop:
            self.forward_velocity = 0
        else:
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
    
    def forward(self):
        if self.forward_velocity < self.max_forward_velocity:
            self.forward_velocity += self.acceleration
    
    def stop(self):
        if self.forward_velocity > 0:
            self.forward_velocity -= self.acceleration
    
    def turn_left(self):
        self.angle -= 3
    
    def turn_right(self):
        self.angle += 3


class Game:
    def __init__(self):
        self.trackList : list[pygame.Rect] = []
        self.gateList : list[tuple[pygame.Rect, int]] = []
        self.running = True
        self.clock = pygame.time.Clock()
        self.create_racetrack1()

    def add_gates(self):
        self.gateList.clear()
        self.gateList.append((pygame.Rect(550, 50, 10, 100), 10))
        self.gateList.append((pygame.Rect(750, 50, 10, 100), 10))
        self.gateList.append((pygame.Rect(950, 50, 10, 100), 10))
        self.gateList.append((pygame.Rect(1050, 250, 100, 10), 10))
        self.gateList.append((pygame.Rect(1000, 350, 10, 100), 10))
        self.gateList.append((pygame.Rect(850, 500, 100, 10), 10))
        self.gateList.append((pygame.Rect(800, 550, 10, 100), 10))
        self.gateList.append((pygame.Rect(650, 500, 100, 10), 10))
        self.gateList.append((pygame.Rect(550, 350, 10, 100), 10))
        self.gateList.append((pygame.Rect(350, 600, 100, 10), 10))
        self.gateList.append((pygame.Rect(50, 600, 100, 10), 10))
        self.gateList.append((pygame.Rect(50, 200, 100, 10), 10))
    
    def create_racetrack1(self):
        self.trackList.append(pygame.Rect(50, 50, 1100, 100))
        self.trackList.append(pygame.Rect(1050, 50, 100, 400))
        self.trackList.append(pygame.Rect(850, 350, 200, 100))
        self.trackList.append(pygame.Rect(850, 450, 100, 200))
        self.trackList.append(pygame.Rect(650, 350, 100, 200))
        self.trackList.append(pygame.Rect(650, 550, 200, 100))
        self.trackList.append(pygame.Rect(350, 350, 300, 100))
        self.trackList.append(pygame.Rect(350, 450, 100, 300))
        self.trackList.append(pygame.Rect(150, 650, 200, 100))
        self.trackList.append(pygame.Rect(50, 150, 100, 200))
        self.trackList.append(pygame.Rect(75, 350, 50, 100))
        self.trackList.append(pygame.Rect(50, 450, 100, 300))
        
        self.add_gates()

    def point_out_of_bounds(self, x, y):
        for rect in self.trackList:
            if rect.collidepoint(x, y):
                return False
        return True
    
    def check_gates(self, car):
        if not self.gateList:
            self.add_gates()
        for gate_rect, gate_points in self.gateList:
            if gate_rect.collidepoint(car.pos):
                car.points += gate_points
                self.gateList.remove((gate_rect, gate_points))
                break
    
    def main_loop(self, display, car):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    car.move(stop=True)
                    self.running = False
            if self.point_out_of_bounds(car.pos[0], car.pos[1]):
                self.on_death()
            car.handle_input()
            self.check_gates(car)
            car.move()
            self.get_sensor_data(car)
            self.clock.tick(60)
            display.draw_scene(self, car)
        pygame.quit()
    
    def on_death(self):
        car.reset()
        car.move(stop=True)
        self.add_gates()

    def car_wall_rays(self, car, angle_offset):
        sensor_angle = car.angle + angle_offset
        sensor_x = car.pos[0]
        sensor_y = car.pos[1]
        for distance in range(1, 400):
            test_x = sensor_x + (distance * math.cos(math.radians(sensor_angle)))
            test_y = sensor_y + (distance * math.sin(math.radians(sensor_angle)))
            if self.point_out_of_bounds(test_x, test_y):
                return distance, test_x, test_y
            if distance >= 399:
                return distance, test_x, test_y
        return 200, sensor_x, sensor_y
    
    def get_sensor_data(self, car):
        sensor_data = []
        for angle_offset in [-45, -22.5, 0, 22.5, 45]:
            distance, x, y = self.car_wall_rays(car, angle_offset)
            sensor_data.append(distance)
        return sensor_data


class DisplayGame:
    def __init__(self, width=1200, height=900):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Display")
        self.width = width
        self.height = height

    def draw_racetrack(self, game):
        track_color = (110, 110, 110)
        for rect in game.trackList:
            pygame.draw.rect(self.screen, track_color, rect, 0)

        gate_color = (0, 0, 200)
        for rect, _ in game.gateList:
            pygame.draw.rect(self.screen, gate_color, rect, 0)

    def draw_ray(self, game, car):
        for angle_offset in [-45, -22.5, 0, 22.5, 45]:
            distance, end_x, end_y = game.car_wall_rays(car, angle_offset)
            pygame.draw.line(self.screen, (0, 255, 0), car.pos, (end_x, end_y), 2)

    def draw_scene(self, game, car):
        self.screen.fill((17, 99, 0))
        self.draw_racetrack(game)
        car.draw(self.screen)
        self.draw_ray(game, car)
        self.draw_stats(game, car)
        pygame.display.flip()
    
    def draw_stats(self, game, car):
        font = pygame.font.SysFont(None, 24)
        speed_text = font.render(f"Speed: {car.forward_velocity:.2f}", True, (255, 255, 255))
        points_text = font.render(f"Points: {car.points}", True, (255, 255, 255))
        timer_text = font.render(f"Time: {pygame.time.get_ticks() // 1000}s", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 10))
        self.screen.blit(points_text, (10, 40))
        self.screen.blit(timer_text, (10, 70))
        

if __name__ == "__main__":
    display = DisplayGame()
    game = Game()
    car = Car()
    game.main_loop(display, car)