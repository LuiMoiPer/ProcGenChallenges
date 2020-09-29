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
                _, _, b = self.pixels[x, y]
                self.pixels[x, y] = (255, 0, b)
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
        normR += self.diffusionRate[R] * self.laplace(x, y, R) - normR * normG ** 2 + self.feedRate * (1 - normR)
        normG += self.diffusionRate[G] * self.laplace(x, y, G) + normR * normG ** 2 - (self.killRate + self.feedRate) * normG

        r *= 255
        g *= 255
        b *= 255

        # keeping values in bounds
        r = 0 if r < 0 else r
        r = 255 if r > 255 else r
        g = 0 if g < 0 else g
        g = 255 if g > 255 else g
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
            sum += self.pixels[x, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.05
            sum += self.pixels[x + 1, y][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.05
        if x is self.image.size[0] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.05
            sum += self.pixels[x - 1, y][channel] / 255 * 0.2
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.05
            sum += self.pixels[x, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.2
        if y is 0:
            sum += self.pixels[x - 1, y][channel] / 255 * 0.2
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.05
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.05
        if y is self.image.size[1] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.05
            sum += self.pixels[x - 1, y][channel] / 255 * 0.2
            sum += self.pixels[x, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.05
            sum += self.pixels[x + 1, y][channel] / 255 * 0.2
        return sum

    def laplaceCorner(self, x, y, channel):
        sum = 0
        if x is 0 and y is 0:
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y][channel] / 255 * 0.2
            sum += self.pixels[x + 1, y + 1][channel] / 255 *  0.05
        if x is 0 and y is self.image.size[1] - 1:
            sum += self.pixels[x, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x + 1, y - 1][channel] / 255 *  0.05
            sum += self.pixels[x + 1, y][channel] / 255 * 0.2
        if x is self.image.size[0] - 1 and y is 0:
            sum += self.pixels[x - 1, y][channel] / 255 * 0.2
            sum += self.pixels[x - 1, y + 1][channel] / 255 *  0.05
            sum += self.pixels[x, y][channel] / 255 * - 1
            sum += self.pixels[x, y + 1][channel] / 255 * 0.2
        if x is self.image.size[0] - 1 and self.image.size[1] - 1:
            sum += self.pixels[x - 1, y - 1][channel] / 255 * 0.05
            sum += self.pixels[x - 1, y][channel] / 255 * 0.2
            sum += self.pixels[x, y - 1][channel] / 255 * 0.2
            sum += self.pixels[x, y][channel] / 255 * - 1
        return sum

if __name__ == "__main__":
    rd = ReactionDiffusion((100, 100))
    rd.seed((49, 49), (3, 3))
    rd.save()