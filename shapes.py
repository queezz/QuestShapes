import numpy as np


class Shape:
    def __init__(self, **kws):
        """"""
        self.scale = kws.get("scale", 1)
        self.origin = kws.get("origin", [0, 0])
        self.rotation = kws.get("rotation", 0)
        self.stretch = kws.get("stretch", [1, 1])
        self.x = np.array(kws["x"]) * self.stretch[0] * self.scale + self.origin[0]
        self.y = np.array(kws["y"]) * self.stretch[1] * self.scale + self.origin[1]
        self.xy = np.array([self.x, self.y])

    def plot(self, **kws):
        import matplotlib.pylab as plt

        plt.plot(*self.xy, **kws)

    def invert(self):
        """ Invert direction """
        self.x = self.x[::-1]
        self.y = self.y[::-1]
        self.xy = np.array([self.x, self.y])


def combineshapes(shapes):
    """take x and y coordinates from a list of shapes
    np.concatenate them and return a new shape"""
    x = np.concatenate([i.x for i in shapes])
    y = np.concatenate([i.y for i in shapes])
    return Shape(x=x, y=y)


class Circle(Shape):
    def __init__(self, **kws):
        """"""
        self.alpha = kws.get("alpha", 0)
        self.beta = kws.get("beta", np.pi * 2)
        n = kws.get("n", 60)
        t = np.linspace(self.alpha, self.beta, n)
        x = np.cos(t)
        y = np.sin(t)
        super().__init__(x=x, y=y, **kws)


class Cross(Shape):
    def __init__(self, **kws):
        """"""
        x = (
            np.array(
                [-1.5, -1.5, -0.5, -0.5, 0.5, 0.5, 1.5, 1.5, 0.5, 0.5, -0.5, -0.5, -1.5]
            )
            / 3
        )
        y = (
            np.array(
                [-0.5, 0.5, 0.5, 1.5, 1.5, 0.5, 0.5, -0.5, -0.5, -1.5, -1.5, -0.5, -0.5]
            )
            / 3
        )
        super().__init__(x=x, y=y, **kws)


class Quest(Shape):
    def __init__(self, **kws):
        """"""
        x = np.array([0.2, 0.2, 0.245, 0.705, 1.38, 1.38, 1.520, 1.520])
        x = np.concatenate((x, x[::-1]))
        y = np.array([0.0, 1.245, 1.394, 1.394, 0.503, 0.498 / 2.0, 0.498 / 2.0, -0.27])
        y = np.concatenate((y, -y[::-1]))
        super().__init__(x=x, y=y, **kws)

    # Divertor plates
    # ax.plot([0.25,0.8],[1,1],'k',lw = vessel_lw)
    # ax.plot([0.25,0.8],[-1,-1],'k',lw = vessel_lw)


class Pshape(Shape):
    def __init__(self, **kws):
        x = np.array([1, 0, 0, 1])
        y = np.array([0.5, 0.5, -0.5, -0.5])
        super().__init__(x=x, y=y, **kws)


class QuestTop(Shape):
    def __init__(self, **kws):
        r0 = kws.get("r0", 0.2)
        r = kws.get("r", 1.38)
        rport = kws.get("rport", 1.52)
        h = kws.get("h", 0.498)
        gamma = np.arcsin(h / 2 / r)  # should connect to r2 circle
        l = rport - r + h / 2 * np.tan(gamma / 2)
        c0 = Circle(scale=r0, alpha=np.pi / 2, beta=np.pi * 3 / 2)
        c0.invert()
        c1 = Circle(scale=r, alpha=np.pi / 2, beta=np.pi - gamma)
        c2 = Circle(scale=r, alpha=np.pi + gamma, beta=np.pi * 3 / 2)
        p = Pshape(stretch=[l, h], origin=[-rport, 0])

        wall = combineshapes([c1, p, c2, c0, Shape(x=c1.x[:1], y=c1.y[:1])])
        super().__init__(x=wall.x, y=wall.y, **kws)
