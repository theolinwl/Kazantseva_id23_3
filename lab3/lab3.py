import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QSpinBox, QSlider,
    QHBoxLayout, QVBoxLayout, QComboBox, QDialog, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import QTimer, Qt
import random
import math
import json


with open('start_param.json', 'r') as file:
    start_param = json.load(file)

num_drops = start_param['num_drops']
drop_colours = start_param['colours']['drops']
cloud_colours = start_param['colours']['clouds']
min_speed = start_param['speed']['min']
max_speed = start_param['speed']['max']
min_angle = start_param['angle']['min']
max_angle = start_param['angle']['max']
min_drop_width = start_param['size']['width']['min']
max_drop_width = start_param['size']['width']['max']
min_drop_height = start_param['size']['height']['min']
max_drop_height = start_param['size']['height']['max']


class Cloud:
    def __init__(self, num_drops=100, speed=None, shape='Эллипс'):
        self.x = random.uniform(0, 800)
        self.y = random.uniform(0, 100)
        self.width = random.randint(60, 150)
        self.height = random.randint(10, 100)
        self.num_drops = num_drops
        self.left_drops = num_drops
        self.speed = speed
        self.shape = shape
        self.colour = random.choice(cloud_colours)
        self.drops = []

        self.create_timer = QTimer()
        self.create_timer.timeout.connect(self.generate_drop)
        self.create_timer.start(10)

    def paint(self, painter):
        painter.setBrush(QColor(self.colour))
        if self.shape == 'Прямоугольник':
            painter.drawRect(
                int(self.x),
                int(self.y),
                self.width,
                self.height
            )
        elif self.shape == 'Эллипс':
            painter.drawEllipse(
                int(self.x),
                int(self.y),
                self.width,
                self.height
            )
        elif self.shape == 'Округлый прямoугольник':
            painter.drawRoundedRect(
                int(self.x),
                int(self.y),
                self.width,
                self.height,
                10,
                10
            )

    def generate_drop(self):
        if self.left_drops > 0:
            self.drops.append(Drop(self))
            self.left_drops -= 1
            self.create_timer.start(
                random.randint(10, 200)
            )
        else:
            self.create_timer.stop()

    def is_clicked(self, point):
        if (self.x < point.x() < self.x + self.width
                and self.y < point.y() < self.y + self.height):
            return True
        return False

    def move(self, point):
        self.x = point.x() - self.width / 2
        self.y = point.y() - self.height / 2


class Drop:
    def __init__(self, cloud, colour=None):
        self.cloud = cloud
        if colour is not None:
            self.colour = colour
        else:
            self.colour = random.choice(drop_colours)
        self.start = (
            random.uniform(self.cloud.x, self.cloud.x + self.cloud.width),
            random.uniform(
                self.cloud.y + 0.8 * self.cloud.height,
                self.cloud.y + 1.2 * self.cloud.height
            )
        )
        self.angle = math.radians(random.uniform(min_angle, max_angle))
        self.x = self.start[0]
        self.y = self.start[1]

    def move(self):
        x = self.cloud.speed * math.sin(self.angle)
        y = self.cloud.speed * math.cos(self.angle)
        self.x += x
        self.y += y

        if self.y > 500:
            self.reset()

    def reset(self):
        self.start = (
            random.uniform(self.cloud.x, self.cloud.x + self.cloud.width),
            random.uniform(
                self.cloud.y + 0.8 * self.cloud.height,
                self.cloud.y + 1.2 * self.cloud.height
            )
        )
        self.colour = random.choice(drop_colours)
        self.angle = math.radians(random.uniform(min_angle, max_angle))
        self.x = self.start[0]
        self.y = self.start[1]

    def paint(self, painter):
        colour = QColor(self.colour)
        painter.fillRect(
            int(self.x),
            int(self.y),
            int(random.uniform(min_drop_width, max_drop_width)),
            int(random.uniform(min_drop_height, max_drop_height)),
            QColor(colour)
        )


class SettingsDialog(QDialog):
    def __init__(self, win, cloud):
        super().__init__(win)
        self.win = win
        self.cloud = cloud
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Параметры облака')
        self.setFixedWidth(300)
        self.layout = QVBoxLayout()

        self.width_slider = QSlider()
        self.width_slider.setRange(60, 150)
        self.width_slider.setOrientation(Qt.Horizontal)
        self.width_slider.setValue(self.cloud.width)
        width_label = QLabel('Ширина')
        self.layout.addWidget(width_label)
        self.layout.addWidget(self.width_slider)

        self.height_slider = QSlider()
        self.height_slider.setRange(10, 100)
        self.height_slider.setOrientation(Qt.Horizontal)
        self.height_slider.setValue(self.cloud.height)
        height_label = QLabel('Высота')
        self.layout.addWidget(height_label)
        self.layout.addWidget(self.height_slider)

        self.num_drops_input = QSpinBox()
        self.num_drops_input.setRange(50, 500)
        self.num_drops_input.setValue(self.cloud.num_drops)
        num_drops_label = QLabel('Плотность')
        self.layout.addWidget(num_drops_label)
        self.layout.addWidget(self.num_drops_input)

        self.speed_slider = QSlider()
        self.speed_slider.setRange(min_speed, max_speed)
        self.speed_slider.setOrientation(Qt.Horizontal)
        self.speed_slider.setValue(self.cloud.speed)
        speed_label = QLabel('Скорость')
        self.layout.addWidget(speed_label)
        self.layout.addWidget(self.speed_slider)

        self.shape_choice = QComboBox()
        self.shape_choice.addItems(
            ['Эллипс', 'Прямоугольник', 'Округлый прямoугольник']
            )
        self.shape_choice.setCurrentText(self.cloud.shape)
        shape_label = QLabel('Форма')
        self.layout.addWidget(shape_label)
        self.layout.addWidget(self.shape_choice)

        self.btn1 = QPushButton('Отменить')
        self.btn1.clicked.connect(self.close)
        self.layout.addWidget(self.btn1)

        self.btn2 = QPushButton('Удалить тучку')
        self.btn2.clicked.connect(self.delete_cloud)
        self.layout.addWidget(self.btn2)

        self.btn3 = QPushButton('Применить изменения', self)
        self.btn3.clicked.connect(self.change_cloud)
        self.layout.addWidget(self.btn3)

        self.setLayout(self.layout)

    def change_cloud(self):
        self.cloud.height = self.height_slider.value()
        self.cloud.width = self.width_slider.value()
        self.cloud.speed = self.speed_slider.value()
        self.cloud.shape = self.shape_choice.currentText()
        self.cloud.num_drops = self.num_drops_input.value()
        self.close()

    def delete_cloud(self):
        self.win.clouds.remove(self.cloud)
        self.close()


class Rain(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 800, 500)
        self.setWindowTitle('Дождь с тучками')
        self.clouds = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(60)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addStretch()
        self.layout = QHBoxLayout()
        cloud_btn = QPushButton('Добавить тучку', self)
        cloud_btn.clicked.connect(self.add_cloud)
        self.layout.addWidget(cloud_btn)

        self.num_drops_input = QSpinBox()
        self.num_drops_input.setRange(50, 500)
        self.num_drops_input.setValue(100)
        num_drops_label = QLabel('Плотность')
        self.layout.addWidget(num_drops_label)
        self.layout.addWidget(self.num_drops_input)

        self.speed_slider = QSlider()
        self.speed_slider.setRange(min_speed, max_speed)
        self.speed_slider.setOrientation(Qt.Horizontal)
        self.speed_slider.setValue(20)
        speed_label = QLabel('Скорость')
        self.layout.addWidget(speed_label)
        self.layout.addWidget(self.speed_slider)

        self.shape_choice = QComboBox()
        self.shape_choice.addItems(
            ['Эллипс', 'Прямоугольник', 'Округлый прямoугольник']
            )
        shape_label = QLabel('Форма')
        self.layout.addWidget(shape_label)
        self.layout.addWidget(self.shape_choice)

        lbl1 = QLabel(self)
        umbrella = QPixmap('umbrella.png').scaled(200, 200, Qt.KeepAspectRatio)
        lbl1.setPixmap(umbrella)
        lbl1.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(lbl1)

        lbl2 = QLabel(self)
        cat = QPixmap('cat.png').scaled(300, 300, Qt.KeepAspectRatio)
        lbl2.setPixmap(cat)
        lbl2.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(lbl2)

        self.main_layout.addLayout(self.layout)

    def add_cloud(self):
        speed = self.speed_slider.value()
        drops_num = self.num_drops_input.value()
        shape = self.shape_choice.currentText()
        new_cloud = Cloud(drops_num, speed, shape)
        self.clouds.append(new_cloud)

    def mousePressEvent(self, event):
        for cloud in self.clouds:
            if cloud.is_clicked(event.pos()):
                self.selected = cloud
                self.dragging = False
                break
            else:
                self.selected = None

    def mouseMoveEvent(self, event):
        if self.selected is not None:
            self.dragging = True
            self.selected.move(event.pos())

    def mouseReleaseEvent(self, event):
        if self.selected is not None and not self.dragging:
            win = SettingsDialog(self, self.selected)
            win.move(350, 200)
            win.exec_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('#e6e6fa'))

        for cloud in self.clouds:
            cloud.paint(painter)
            for drop in cloud.drops:
                drop.move()
                drop.paint(painter)


def main():
    app = QApplication(sys.argv)
    rain = Rain()
    for _ in range(2):
        rain.add_cloud()
    rain.show()
    sys.exit(app.exec_())


main()
