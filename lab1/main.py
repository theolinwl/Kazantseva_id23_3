from tkinter import Tk, Canvas
import math

size = 600
rad = 200
angle = 0
# обрабатываем ввод пользователя, задающий скорость
while True:
    try:
        print('Введите скорость движения. '
              'Чем ближе значение к 0, тем быстрее движение.')
        speed = math.pi / float(input('Положительное значение — '
                                      'по часовой стрелке, '
                                      'отрицательное — против: '))
        break
    except (ValueError, ZeroDivisionError):
        print('Попробуйте снова')

# создаем окно
root = Tk()
root.title('Круг с движущейся точкой')

# создаем холст и кладем его в наше окно
canvas = Canvas(root, width=size, height=size, bg='white')
canvas.pack()

# на холсте создаем круг
canvas.create_oval(size/2 - rad, size/2 - rad,
                   size/2 + rad, size/2 + rad, width=2)
root.update()


def moving_point(angle, speed):
    angle = angle + speed  # угол изменяется в соответствии со скоростью
    x0, y0 = size/2 + rad * math.cos(angle), size/2 + rad * math.sin(angle)

    # обновляем координаты точки
    canvas.coords(dot, x0 - 10, y0 - 10, x0 + 10, y0 + 10)
    root.after(30, moving_point, angle, speed)


x, y = size/2 + rad, size/2  # точка создается, где угол 0 от центра
dot = canvas.create_oval(x - 10, y - 10, x + 10, y + 10,
                         fill='blue', outline='', width=0)
root.after(30, moving_point, angle, speed)  # спустя время запускаем функцию

root.mainloop()
