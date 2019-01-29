import csv
import math
from PIL import Image, ImageDraw
from random import randint

class WindroseDraw(ImageDraw.ImageDraw):
    def __init__(self, im, radius, width, center = None, mode = None):
        """ Create a drawing instance for windrose diagrams.
        :param im: The Image to draw in.
        :param radius: The radius of the center circle around which the bars are placed.
        :param width: The width of the individual bars.
        :param center: The center around which the windrose is plotted. If omitted, the center defaults to the center of the image.
        """
        super().__init__(im, mode)
        self.radius = radius
        self.width = width
        if center:
            self.center = center
        else:
            self.center = (int(im.width / 2), int(im.height / 2))

    def _rotate(self, point, center, angle):
        """ rotate a point around a center
        point   : two-tupel (x,y) of the point to rotate
        center  : two-tupel (x,y) of the center
        angle   : angle at which the point is to be rotated
        """
        newX = center[0] + (point[0] - center[0]) * math.cos(angle) - (point[1] - center[1]) * math.sin(angle)
        newY = center[1] + (point[0] - center[0]) * math.sin(angle) + (point[1] - center[1]) * math.cos(angle)
        return (newX, newY)
        
    def bar(self, height, angle, *args):
        """ draws an individial bar of a windrose diagram
        :param height: The height of the bar to draw.
        :param angle: The angle at which the bar is rotated.
        """

        halfWidth = int(self.width / 2)
        pos = [
                (self.center[0] - halfWidth, self.center[1] + self.radius),
                (self.center[0] - halfWidth, self.center[1] + self.radius + height),
                (self.center[0] + halfWidth, self.center[1] + self.radius + height),
                (self.center[0] + halfWidth, self.center[1] + self.radius)
            ]
        rotated_pos = [self._rotate(p, self.center, angle) for p in pos]
        self.polygon(rotated_pos, *args)



def windrose():
    """ Function to generate a windrose Image """
    width = 500
    height = 500
    center = (int(width / 2), int(height / 2))
    im = Image.new('RGB', (width, height), '#ffffff')
    draw = WindroseDraw(im, 40, 8)
    for x in range(0,360,30):
        draw.bar(randint(10, 200), math.radians(x), '#330099')
    im.show()
    

#stations = []
#with open('./all_stations_metdb.csv', encoding = 'latin1') as csvfile:
    #reader = csv.DictReader(csvfile, delimiter = ',')
    #for row in reader:
        #stations.append(dict(row))

#print(stations[0])

#n000 = max([s.get('n000') for s in stations])
#print(stations[0].keys())

windrose()

