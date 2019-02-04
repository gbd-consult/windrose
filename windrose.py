import math
from PIL import Image, ImageDraw, ImageFont

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
        self.image = im
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

    def circle(self, radius, center = None, **kwargs):
        """ Draws a circle of a given radius around a center.
        :param radius: The radius of the circle.
        :param center: The center of the circle. Defaults to the center of the plot.
        """
        if not center:
            center = self.center
        self.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), **kwargs)

    def rotatedText(self, text, position, angle, **kwargs):
        """ Draws the string at the given position and rotates it over the center.
        :param text: Text to be drawn.
        :param position: Top left corner of the text.
        :param angle: angle at which to rotate the text.
        """
        im_new = Image.new('RGBA', self.image.size, '#00000000')
        draw = ImageDraw.Draw(im_new)
        draw.text(position, text, **kwargs)
        im_rotated = im_new.rotate(angle)
        self.image.paste(im_rotated, mask = im_rotated)
        



def windrose(nlist, ntotal, id, station, net, start, end, hasl, hagr, avgff, calm):
    """ Function to generate a windrose Image.
    :param nlist: List of number of occurences for each wind direction.
    :param ntotal: total number of wind direction measurements.
    :param id: id of the weather station.
    :param station: name of the weather station.
    :param net: network to which the weather station belongs.
    :param start: start date of measurements.
    :param end: end date of measurements.
    :param hasl: height above sea level of the station (m).
    :param hagr: height of measurent above station.
    :param avgff: Average FF (m/s).
    :param calm: number of measurements with FF < 0.5.
    """
    bg_color = '#ffffff'
    fg_color = '#000000'
    bar_color = '#4CB29C'
    width = 700
    height = 800
    header_height = 100
    margin = 50
    inner_radius = 60
    outer_radius = (width / 2 - margin) - inner_radius
    bar_width = 12
    center = (int(width / 2), int((height - header_height) / 2) + header_height)
    
    try:
        font = ImageFont.truetype('arial.ttf', 18)
    except:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 16)
        except:
            font = ImageFont.load_default()

    im = Image.new('RGB', (width, height), bg_color)
    draw = WindroseDraw(im, inner_radius, bar_width, center = center)

    values_perc = [v / ntotal * 100 for v in nlist]

    # autoscale to maximum in 5 percent steps
    scale_max = [y for y in range(100, int(max(values_perc)), -1 ) if y % 5 == 0].pop()
    scale_factor = outer_radius / scale_max
    values_scaled = [v * scale_factor for v in values_perc]

    # draw scale
    for x in range(0, scale_max + 5, 5):
        r = x * scale_factor + inner_radius
        draw.circle(r, outline = fg_color)
        draw.text((center[0] + r + 5, center[1] + 10), '%s%%' % x, fill = fg_color, font = font)

    # draw cross
    dirs = [    (0, -1, 'N'),
                (+1, 0, 'E'),
                (0, +1, 'S'),
                (-1, 0, 'W')]
    for d in dirs:
        draw.line([ ((center[0] + (d[0] * inner_radius)), (center[1] + (d[1] * inner_radius))),
                    ((center[0] + (d[0] * (inner_radius + outer_radius))), (center[1] + (d[1] * (inner_radius + outer_radius))))],
                    fill = fg_color)
        text_size = font.getsize(d[2])
        radius = inner_radius + outer_radius + 5
        draw.text(((center[0] + (d[0] * (radius + text_size[0])) - (0.5 * text_size[0])), (center[1] + (d[1] * (radius + text_size[1])) - (0.5 * text_size[1]))),
            d[2], fill = fg_color, font = font)

    # draw the bars
    for x in range(0,360,30):
        draw.bar(values_scaled[int(x / 30)], math.radians(x + 180), bar_color)

    # draw metadata header
    metadata = "%s %s   %s\n%s - %s\n%s m NHN  %s m GOK  %.2f m/s" % (net, id, station, start, end, hasl, hagr, avgff)
    draw.line([(0, header_height), (width, header_height)], fill = fg_color)
    draw.text((margin / 2,margin / 2), metadata, font = font, fill = fg_color)

    # draw calm percentage
    calm_perc = calm / ntotal * 100
    calm_text = "%.2f %%" % calm_perc
    calm_size = font.getsize(calm_text)
    draw.text(((center[0] - calm_size[0] / 2), (center[1] - calm_size[1] / 2)), calm_text, font = font, fill = fg_color)
    
    im.show()
