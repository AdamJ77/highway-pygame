import pygame as pg

from config import HEIGHT, WIDTH


class Environment:
    def __init__(self, clouds, highway_background, lamps) -> None:
        self.clouds = clouds
        self.highway_background = highway_background
        self.lamps = lamps


class GUI:
    def __init__(self, window, fonts: dict=None) -> None:
        self.fonts = fonts if fonts is not None else {}
        self.window = window
        self.colors = {"black": (0, 0, 0), "white": (255, 255, 255)}
        self.add_font("Raleway-Regular", "Raleway-Regular.ttf", 36)

    def add_font(self, font_name: str, path, size: int):
        font = pg.font.Font(path, size)
        self.fonts[font_name] = font

    def get_text_object(self, text: str, font_name: str, text_color: tuple, bg_color: tuple=None):
        return self.fonts.get(font_name).render(text, True, text_color, bg_color)
    
    def set_text(self, text_object: pg.font.Font.render, x_pos, y_pos):
        text_rect = text_object.get_rect()
        text_rect.center = (x_pos, y_pos)
        return text_rect

    def display_text(self, window, text, text_rect):
        window.blit(text, text_rect)


class VelocityGUI(GUI):
    def __init__(self, window, velocity_delay: int, fonts: dict = None) -> None:
        super().__init__(window, fonts)
        self.velocity_delay = velocity_delay
        self.delay_counter = 1
        self.speed_text = self.get_text_object(f"0.00 KM/H", "Raleway-Regular", self.colors.get("black"), self.colors.get("white"))
        self.speed_text_rect = self.set_text(self.speed_text, WIDTH // 2, HEIGHT - 30)
    
    # def __getattr__(self, _attr):
    #     if hasattr(self.colors, _attr):
    #         return getattr(self.colors, _attr)
    #     else:
    #         raise AttributeError

    def display_velocity(self, speed: float):
        if self.delay_counter % self.velocity_delay != 0:
            self.delay_counter += 1
        else:
            self.delay_counter = 1
            self.change_velocity_text(speed)
        self.display_text(self.window, self.speed_text, self.speed_text_rect)

    def change_velocity_text(self, speed: float):
        self.speed_text = self.get_text_object(f"{speed:.2f} KM/H", "Raleway-Regular", self.colors.get("black"), self.colors.get("white"))


class CollisionGUI(GUI):
    def __init__(self, window, fonts: dict = None) -> None:
        super().__init__(window, fonts)
        self.add_font("Raleway-Regular", "Raleway-Regular.ttf", 32)
        self.collis_counter: int= 0

    def display_collisions_counter(self):
        pass

    def __repr__(self) -> str:
        return f"Collisions: {self.collis_counter}"


class TimerGUI(GUI):
    def __init__(self, window, fonts: dict = None) -> None:
        super().__init__(window, fonts)
        pass