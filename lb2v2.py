import time
from math import sin, cos, fabs


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Scene:
    def __init__(self):
        self._figures = []

    def add_figures(self, figure):
        self._figures.append(figure)

    def render(self, x, y, width, height, m, n):

        matrix = [['  ' for _ in range(n)] for _ in range(m)]

        dx = width / n
        dy = height / m

        for i in range(n):
            for j in range(m):
                cx = x + j * dx
                cy = y + i * dy

                for f in self._figures:
                    if f.contain(cx, cy):
                        matrix[i][j] = '+ '
                        break

        return matrix


class Shape:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    @property
    def left(self):
        return self._x

    @property
    def right(self):
        return self._x + self._width

    @property
    def top(self):
        return self._y

    @property
    def bottom(self):
        return self._y + self._height

    def contain(self, x, y):
        return (self.left <= x < self.right) and \
            (self.top <= y < self.bottom)


class Coord:
    def __init__(self, dx=0, dy=0, angle=0, parent=None):
        self._dx = dx
        self._dy = dy
        self._a = angle
        self._parent = parent

    def map_to_parent(self, x, y):
        # # '''Not working'''
        # if self._a == 0:
        #     self._parent.total_dx = obj._x - self._dx
        #     self._parent.total_dy = obj._y - self._dy
        # elif self._a != 0:
        #     self._parent.total_dx = (obj._x - self._dx) * cos(self._a) + \
        #                              (obj._y - self._dy) * sin(self._a)
        #     self._parent.total_dy = -(obj._x - self._dx) * sin(self._a) + \
        #                              (obj._y - self._dy) * cos(self._a)
        return (cos(self._a) * x - sin(self._a) * y + self._dx,
                sin(self._a) * x + cos(self._a) * y + self._dy)

    def map_to_absolute(self, x, y):
        if self._a == 0:
            return self.map_to_absolute(*self.map_to_parent(x, y))
        elif self._a != 0:
            return self.map_to_parent(x, y)

    # # '''Not working'''
    # if self._a == 0:
    #     obj._x = self._parent.total_dx + self._dx
    #     obj._y = self._parent.total_dy + self._dy
    # elif self._a != 0:
    #     obj._x = self._parent.total_dx * cos(self._a) - \
    #              self._parent.total_dx * sin(self._a) + self._dx
    #     obj._y = self._parent.total_dy * sin(self._a) + self._parent.total_dy * cos(self._a) + self._dy


class Polygon:
    def __init__(self, x, y, n, coord=None):
        self._x = x
        self._y = y
        self._n = n
        self._coord = coord
        self._pp = Point(x, y)

    # list = []
    # for i in range(self._n + 1):
    #     list.append(self._coord.map_to_absolute(self._pp.x[i], self._pp.y[i]))
    # return list
    def points(self):
        if self._coord is None:
            pass
        else:
            for i in range(self._n + 1):
                self._pp.x[i % self._n], self._pp.y[i % self._n] = self._coord.map_to_absolute(
                    self._pp.x[i % self._n], self._pp.y[i % self._n]
                )

    def contain(self, x, y):
        # if Inside_Polygon(self._pp, self._n, x, y) and (min(self._pp.x) <= x <= max(self._pp.x)) \
        #         and (min(self._pp.y) <= y <= max(self._pp.y)):
        if inside_polygon(self._pp, self._n, x, y):
            return True


'''
class Ellipse(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def contain(self, x, y):
        return ((x - self._x) ** 2 / (self._width / 2) ** 2 +
                (y - self._y) ** 2 / (self._height / 2) ** 2) <= 1
'''


class MovingObject:
    def __init__(self, x, y, v, g=None):
        self._y = y
        self._x = x
        self._vx = v
        self._vy = 0
        self._g = g

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def recalc_ph(self, dt):
        self._x += self._vx * dt
        vy = self._vy
        self._vy += self._g * dt
        self._y += (self._vy / 2 + vy) * dt

        if self._y >= 11:
            self._y = 10
            self._vy = -self._vy * 0.7


def inside_polygon(polygon, number_of_vertices, x, y):
    """
    параметры функции:
    polygon - полигон
    number_of_vertices - кол-во вершин у полигона
    x - x-координата точки
    y - y-координата точки
    """
    global flag
    count = 0
    for n in range(number_of_vertices):
        flag = False
        if n < number_of_vertices - 1:
            i1 = n + 1
        else:
            i1 = 0
        while not flag:
            i2 = i1 + 1
            if i2 >= number_of_vertices:
                i2 = 0
            S = fabs(
                polygon.x[i1] * (polygon.y[i2] - polygon.y[n]) + polygon.x[i2] * (polygon.y[n] - polygon.y[i1]) +
                polygon.x[n] * (polygon.y[i1] - polygon.y[i2]))
            S1 = fabs(polygon.x[i1] * (polygon.y[i2] - y) + polygon.x[i2] * (y - polygon.y[i1]) + x * (
                    polygon.y[i1] - polygon.y[i2]))
            S2 = fabs(polygon.x[n] * (polygon.y[i2] - y) + polygon.x[i2] * (y - polygon.y[n]) + x * (
                    polygon.y[n] - polygon.y[i2]))
            S3 = fabs(polygon.x[i1] * (polygon.y[n] - y) + polygon.x[n] * (y - polygon.y[i1]) + x * (
                    polygon.y[i1] - polygon.y[n]))
            if S == S1 + S2 + S3:
                flag = True
                break
            i1 = i1 + 1
            if i1 >= number_of_vertices:
                i1 = 0
            count += 1
            if count >= 3:
                break
    return flag


k = 0
scene = Scene()
absolute = Coord(0, 0)
plane1 = Coord(20, 15, 30)
plane2 = Coord(50, 50, 60, plane1)
plane3 = Coord(0, 0, 1)
plane4 = Coord(0, 0, 90, plane3)
r = Rectangle(7, 3, 1, 1)
p1 = Polygon([1, 5, 10], [1, 5, 1], 3, plane4)
# p4 = Polygon([10, 20, 20, 10], [5, 5, 1, 1], 4, plane3)
scene.add_figures(r)
scene.add_figures(p1)
# scene.add_figures(p4)
# scene.add_figures(Rectangle(2.5, 4.2, 1, 2))
# e = Ellipse(5, 2, 3, 2)
# scene.add_figures(e)
mo1 = MovingObject(7, 3, 0.5, 9.8)
mo2 = MovingObject(5, 5, 0.5, 9.81)
while k <= 100:
    m = scene.render(0, 0, 40, 20, 100, 100)
    sc = '\n'.join(''.join(line) for line in m)
    print(sc)
    print(k)
    k += 1
    time.sleep(0.001)
    mo1.recalc_ph(0.1)
    r.x = mo1.x
    r.y = mo1.y
    p1.points()
    mo2.recalc_ph(0.01)
    # a = input()
    # e.x = mo2.x
    # e.y = mo2.y
# m = scene.render(0, 0, 40, 20, 100, 100)
# sc = '\n'.join(''.join(line) for line in m)
# print(sc)
# print(k)
# k += 1
# time.sleep(0.1)
# mo1.recalc_ph(0.1)
# r.x = mo1.x
# r.y = mo1.y
#
# mo2.recalc_ph(0.01)
# # e.x = mo2.x
# # e.y = mo2.y
