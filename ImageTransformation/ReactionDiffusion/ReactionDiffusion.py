from PIL import Image, ImageColor, ImageShow
from time import time

R = 0
G = 1
B = 2
A = 3

class ReactionDiffusion:
    def __init__(self, dimmensions):
        self.image = Image.new("RGB", dimmensions, ImageColor.getrgb("#00ff00"))
        self.pixels = self.image.load()
        self.diffusionRate = (1.0, 0.5)
        self.feedRate = 0.055
        self.killRate = 0.062

    def step(self):
        next = Image.new("RGB", self.image.size)
        next_pixels = next.load()
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                next_pixels[x, y] = self.next_color(x, y)
        self.image = next

    def seed(self, corner, dimmensions):
        x, y = corner
        while x < corner[0] + dimmensions[0]:
            y = corner[1]
            while y < corner[1] + dimmensions[1]:
                _, g, b = self.pixels[x, y]
                self.pixels[x, y] = (255, g, b)
                y += 1
            x += 1

    def save(self, name = None):
        if name is not None:
            self.image.save(f"./outputs/{name}.png")
        else:
            self.image.save(f"./outputs/{time()}.png")


    def show(self):
        ImageShow.show(self.image)

    def next_color(self, x, y):
        r, g, b = self.pixels[x, y]

        # use normalized value between 0 and 1
        normR, normG = r / 255, g / 255

        diffusionRate = self.diffusionRate[R]
        laplace = self.laplace(x, y, R)
        reaction = normR * normG ** 2
        feed = self.feedRate * (1 - normR)
        # normR += self.diffusionRate[R] * self.laplace(x, y, R) - normR * normG ** 2 + self.feedRate * (1 - normR)
        normR += diffusionRate * laplace - reaction + feed

        diffusionRate = self.diffusionRate[G]
        laplace = self.laplace(x, y, G)
        reaction = normR * normG ** 2
        kill = (self.killRate + self.feedRate) * normG
        # normG += self.diffusionRate[G] * self.laplace(x, y, G) + normR * normG ** 2 - (self.killRate + self.feedRate) * normG
        normG += diffusionRate * laplace + reaction - kill

        r = normR * 255
        g = normG * 255

        # keeping values in bounds
        r = 0 if r < 0 else int(r)
        r = 255 if r > 255 else int(r)
        g = 0 if g < 0 else int(g)
        g = 255 if g > 255 else int(g)
        return (r, g, b)

    def laplace(self, x, y, channel):
        # normal
        if (x is not 0 and x is not self.image.size[0] - 1
            and y is not 0 and y is not self.image.size[1] - 1
        ):
            return self.laplaceNormal(x, y, channel)
        # corner
        elif ((x is 0 and y is 0)
            or (x is 0 and y is self.image.size[1] - 1)
            or (x is self.image.size[0] - 1 and y is 0)
            or (x is self.image.size[0] - 1 and y is self.image.size[1] - 1)
        ):
            return self.laplaceCorner(x, y, channel)
        # edge
        else:
            return self.laplaceEdge(x, y, channel)

    def laplaceNormal(self, x, y, channel):
        sum = 0
        sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.05
        sum += self.pixels[x - 1, y][channel] / 255 * 0.2
        sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.05
        sum += self.pixels[x, y - 1][channel] / 255 * 0.2
        sum += self.pixels[x, y][channel] / 255 * - 1
        sum += self.pixels[x, y + 1][channel] / 255 * 0.2
        sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.05
        sum += self.pixels[x + 1, y][channel] / 255 * 0.2
        sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.05
        return sum

    def laplaceEdge(self, x, y, channel):
        sum = 0
        if x is 0:
            sum += self.pixels[x, y - 1][channel] / 255 * 0.25
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.25
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.125
            sum += self.pixels[x + 1, y][channel] / 255 * 0.25
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.125
        if x is self.image.size[0] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.125
            sum += self.pixels[x - 1, y][channel] / 255 * 0.25
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.125
            sum += self.pixels[x, y - 1][channel] / 255 * 0.25
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.25
        if y is 0:
            sum += self.pixels[x - 1, y][channel] / 255 * 0.25
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.125
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.25
            sum += self.pixels[x + 1, y][channel] / 255 * 0.25
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.125
        if y is self.image.size[1] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.125
            sum += self.pixels[x - 1, y][channel] / 255 * 0.25
            sum += self.pixels[x, y - 1][channel] / 255 * 0.25
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.125
            sum += self.pixels[x + 1, y][channel] / 255 * 0.25
        return sum

    def laplaceCorner(self, x, y, channel):
        sum = 0
        if x is 0 and y is 0:
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.4
            sum += self.pixels[x + 1, y][channel] / 255 * 0.4
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.2
        if x is 0 and y is self.image.size[1] - 1:
            sum += self.pixels[x, y - 1][channel] / 255 * 0.4
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.2
            sum += self.pixels[x + 1, y][channel] / 255 * 0.4
        if x is self.image.size[0] - 1 and y is 0:
            sum += self.pixels[x - 1, y][channel] / 255 * 0.4
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.4
        if x is self.image.size[0] - 1 and self.image.size[1] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x - 1, y][channel] / 255 * 0.4
            sum += self.pixels[x, y - 1][channel] / 255 * 0.4
            sum += self.pixels[x, y][channel] / 255 * - 1
        return sum

if __name__ == "__main__":
    rd = ReactionDiffusion((3, 3))
    rd.seed((1, 1), (1, 1))
    for i in range(10):
        rd.step()
        rd.save()