import pygame
import numpy as np
import math
import random

# Colors' initialization
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (230, 231, 232)

# There are parameters of our window (initialization)
WIDTH = 1000
HEIGHT = 800
# Set title
pygame.display.set_caption("Third lab (group: 0323, team: 4)")
# Set window's parameters
window = pygame.display.set_mode((WIDTH, HEIGHT))

position = [WIDTH / 2, HEIGHT / 2]

points = []

yAngle = 0
zAngle = 0
xAngle = 0

points = []

projectionMatrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])

projectedPoints = [
    [n, n] for n in range(4)
]

def connectPoints(points):
    temp = []
    for w in np.arange(0, 1.2, 0.2):
        temp.append([])
        for u in np.arange(0, 1.2, 0.2):
            p2 = np.dot(points[0], (1 - u) * (1 - w)) + np.dot(points[1], (1 - u) * w) + np.dot(points[2], u * (1 - w)) + np.dot(points[3], u * w)
            temp[len(temp) - 1].append(p2)
            pygame.draw.circle(window, BLUE, (p2[0], p2[1]), 2)
    for i in range(0, len(temp) - 1):
        for j in range(0, len(temp)):
            pygame.draw.line(window, GREEN, (temp[j][i][0], temp[j][i][1]), (temp[j][i + 1][0], temp[j][i + 1][1]))
    for i in range(0, len(temp) - 1):
        for j in range(0, len(temp)):
            pygame.draw.line(window, GREEN, (temp[i][j][0], temp[i][j][1]), (temp[i + 1][j][0], temp[i + 1][j][1]))

def displaySurface():
    i = 0
    for point in points:
        rotated2D = np.dot(yRotation, point.reshape(4, 1))
        rotated2D = np.dot(xRotation, rotated2D)
        rotated2D = np.dot(zRotation, rotated2D)

        projected2D = np.dot(projectionMatrix, rotated2D)

        x = int(projected2D[0][0] + position[0])
        y = int(projected2D[1][0] + position[1])

        projectedPoints[i] = [x, y]
        pygame.draw.circle(window, RED, (x, y), 2)
        i += 1

    if (len(points) == 4):
        connectPoints(projectedPoints)

clock = pygame.time.Clock()

while True:

    clock.tick(60)

    xRotation = np.matrix([
        [1, 0, 0, 0],
        [0, math.cos(xAngle), -math.sin(xAngle), 0],
        [0, math.sin(xAngle), math.cos(xAngle), 0],
        [0, 0, 0, 1],
    ])

    yRotation = np.matrix([
        [math.cos(yAngle), 0, math.sin(yAngle), 0],
        [0, 1, 0, 0],
        [-math.sin(yAngle), 0, math.cos(yAngle), 0],
        [0, 0, 0, 1],
    ])

    zRotation = np.matrix([
        [math.cos(zAngle), -math.sin(zAngle), 0, 0],
        [math.sin(zAngle), math.cos(zAngle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                yAngle -= 0.1
            if event.key == pygame.K_UP:
                yAngle += 0.1
            if event.key == pygame.K_RIGHT:
                xAngle -= 0.1
            if event.key == pygame.K_LEFT:
                xAngle += 0.1
            if event.key == pygame.K_1:
                zAngle += 0.1
            if event.key == pygame.K_2:
                zAngle -= 0.1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                xAngle = 0
                yAngle = 0
                zAngle = 0
                if (len(points) < 4):
                    points.append(np.matrix([event.pos[0] - position[0], event.pos[1] - position[1], random.randint(0, 200), 1]))
                    print(points)
            elif event.button == 3:
                xAngle = 0
                yAngle = 0
                zAngle = 0
                if (points):
                    points.pop()
                print(points)

    # Make window's color white
    window.fill(WHITE)
    displaySurface()

    pygame.display.update()