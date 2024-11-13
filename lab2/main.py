import tkinter as tk
import random
import math
import json

root = tk.Tk()
root.title('Дождь')

with open('start_param.json', 'r') as file:
    start_param = json.load(file)

num_drops = start_param['num_drops']
density = start_param['density']
min_speed = start_param['speed']['min']
max_speed = start_param['speed']['max']
min_angle = start_param['angle']['min']
max_angle = start_param['angle']['max']
min_width = start_param['size']['width']['min']
max_width = start_param['size']['width']['max']
min_height = start_param['size']['height']['min']
max_height = start_param['size']['height']['max']

canvas = tk.Canvas(root, width=800, height=500, bg='#e6e6fa')
canvas.pack()


class Drop:
    def __init__(self, speed=None, density_choice=None):
        if speed is not None:
            self.speed = speed
        else:
            self.speed = random.uniform(min_speed, max_speed)

        if density_choice is not None:
            self.density = density_choice
        else:
            self.density = random.choice(density)
        self.start = (random.uniform(0, 800), -200)
        self.angle = math.radians(random.uniform(min_angle, max_angle))
        self.drop = self.create()

    def create(self):
        x0, y0 = self.start
        drop = canvas.create_rectangle(
            x0,
            y0,
            x0 + random.uniform(min_width, max_width),
            y0 - random.uniform(min_height, max_height),
            fill=self.density,
            outline='')
        return drop

    def move(self):
        x = self.speed * math.sin(self.angle)
        y = self.speed * math.cos(self.angle)
        canvas.move(self.drop, x, y)
        coords = canvas.coords(self.drop)

        if coords[1] > canvas.winfo_height():
            self.reset()
            canvas.after(60, self.move)
        else:
            canvas.after(60, self.move)

    def reset(self):
        self.start = (random.uniform(0, 800), -200)
        self.speed = random.uniform(min_speed, max_speed)
        self.density = random.choice(density)
        self.angle = math.radians(random.uniform(min_angle, max_angle))
        canvas.delete(self.drop)
        self.drop = self.create()


def main():
    for _ in range(num_drops):
        drop = Drop()
        drop.move()


main()
root.mainloop()
