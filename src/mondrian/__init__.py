# Mondrian Art Generator, by Al Sweigart al@inventwithpython.com
# Randomly generates PNG images of Mondrian-style art.

# This program requires Pillow, install it with `pip install pillow`

__version__ = '0.0.1'

from PIL import Image, ImageDraw
import random
import logging
logging.basicConfig(filename='mondrian_log.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')

WHITE = 0
BLACK = 1
RED = 2
YELLOW = 3
BLUE = 4
COLOR_MAPPING = {WHITE: 'white', BLACK: 'black', RED: 'red', YELLOW: 'yellow', BLUE: 'blue'}

def createMondrianArt(filename, width, height, min_x_increase, max_x_increase, min_y_increase, max_y_increase, numPaintedRects, numDeletedSegments, scale):
    logging.debug('Starting painting %s...' % (filename))
    logging.debug('width, height = %s, %s' % (width, height))
    logging.debug('min_x_increase, max_x_increase = %s, %s' % (min_x_increase, max_x_increase))
    logging.debug('min_y_increase, max_y_increase = %s, %s' % (min_y_increase, max_y_increase))
    logging.debug('numPaintedRects = %s' % (numPaintedRects))
    logging.debug('numDeletedSegments  = %s' % (numDeletedSegments))

    # Pre-populate the canvas with white space:
    canvas = {} # The data structure that stores the pixel info is a dictionary with (x, y) tuple keys.
    for x in range(width):
        for y in range(height):
            canvas[(x, y)] = WHITE

    # Generate vertical lines:
    x = random.randint(min_x_increase, max_x_increase)
    while x < width - min_x_increase: # Keep generating vertical lines until x gets close to the right edge.
        for y in range(height): # "Draw" a vertical line to the canvas data structure.
            canvas[(x, y)] = BLACK
        x += random.randint(min_x_increase, max_x_increase)

    # Generate horizontal lines:
    y = random.randint(min_y_increase, max_y_increase)
    while y < height - min_y_increase: # Keep generating horizontal lines until y gets close to the bottom edge.
        for x in range(width): # # "Draw" a horizontal line to the canvas data structure.
            canvas[(x, y)] = BLACK
        y += random.randint(min_y_increase, max_y_increase)

    # Randomly select points and try to delete a segment.
    for i in range(numDeletedSegments):
        failedAttemptsToDeleteSegment = 0
        while failedAttemptsToDeleteSegment < 500: # Give up trying to find a segment to delete if we fail 500 times in a row.
            failedAttemptsToDeleteSegment += 1

            # Get a random start point on an existing segment:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)
            if canvas[(startx, starty)] == WHITE:
                continue # This random start point is not on a segment, so get a new rando start point.

            # Find out if we're on a vertical or horizontal segment:
            if canvas[(startx - 1, starty)] == canvas[(startx + 1, starty)] == WHITE:
                orientation = 'vertical'
            elif canvas[(startx, starty - 1)] == canvas[(startx, starty + 1)] == WHITE:
                orientation = 'horizontal'
            else:
                continue # The start point is on an intersection, so get a new random start point.

            pointsToDelete = [(startx, starty)] # The (x, y) points of the segment are recorded in pointsToDelete to delete later.

            foundTIntersection = True
            if orientation == 'vertical':
                for changey in (-1, 1): # On the first iteration, we move up, next iteration we move down.
                    y = starty
                    while 0 < y < height - 1:
                        y += changey # Continue moving until we find a four-way intersection, T-intersection, or edge.
                        if canvas[(startx - 1, y)] == canvas[(startx + 1, y)] == BLACK:
                            # The pixels to the left and right of (startx, y) are black.
                            # We've found a four-way intersection.
                            break
                        elif ((canvas[(startx - 1, y)] == WHITE and
                               canvas[(startx + 1, y)] == BLACK) or
                              (canvas[(startx - 1, y)] == BLACK and
                               canvas[(startx + 1, y)] == WHITE)):
                            # One pixel to the left or right of (startx, y) is black.
                            # We've found a T-intersection; we can't delete this segment.
                            foundTIntersection = False
                            break
                        else:
                            pointsToDelete.append((startx, y))

            elif orientation == 'horizontal':
                for changex in (-1, 1): # On the first iteration, we move left, next iteration we move right.
                    x = startx
                    while 0 < x < width - 1:
                        x += changex # Continue moving until we find a four-way intersection, T-intersection, or edge.
                        if canvas[(x, starty - 1)] == canvas[(x, starty + 1)] == BLACK:
                            # The pixels above and below of (x, starty) are black.
                            # We've found a four-way intersection.
                            break
                        elif ((canvas[(x, starty - 1)] == WHITE and
                               canvas[(x, starty + 1)] == BLACK) or
                              (canvas[(x, starty - 1)] == BLACK and
                               canvas[(x, starty + 1)] == WHITE)):
                            # One pixel above or below of (x, starty) is black.
                            # We've found a T-intersection; we can't delete this segment.
                            foundTIntersection = False
                            break
                        else:
                            # This is a point we can delete (if we can delete this segment).
                            pointsToDelete.append((x, starty))

            if not foundTIntersection:
                # A T-intersection means we can't delete this segment.
                # Start over and get a new random start point.
                continue
            else:
                break # Move on to delete the segment.

        # If we can delete this segment, set all the points in the segment to white:
        for x, y in pointsToDelete:
            canvas[(x, y)] = WHITE

    # Add the border lines at the top, bottom, left, and right edges:
    for x in range(width):
        canvas[(x, 0)] = BLACK # Top border.
        canvas[(x, height - 1)] = BLACK # Bottom border.
    for y in range(height):
        canvas[(0, y)] = BLACK # Left border.
        canvas[(width - 1, y)] = BLACK # Right border.

    # Paint some of the rectangles:
    for i in range(numPaintedRects):
        failedAttemptsToPaintRectangle = 0
        while failedAttemptsToPaintRectangle < 500:
            failedAttemptsToPaintRectangle += 1

            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)

            if canvas[(startx, starty)] != WHITE:
                continue # Get a new random start point.
            else:
                break

        # Flood fill algorithm:
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([(startx, starty)])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            canvas[(x, y)] = colorToPaint
            if canvas[(x - 1, y)] == WHITE:
                pointsToPaint.add((x - 1, y))
            if canvas[(x + 1, y)] == WHITE:
                pointsToPaint.add((x + 1, y))
            if canvas[(x, y - 1)] == WHITE:
                pointsToPaint.add((x, y - 1))
            if canvas[(x, y + 1)] == WHITE:
                pointsToPaint.add((x, y + 1))

    # Draw the image based on the `canvas` data structure:
    im = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(im)
    for y in range(height):
        for x in range(width):
            draw.point((x, y), COLOR_MAPPING[canvas[(x, y)]])

    im = im.resize((width * scale, height * scale))
    im.save(filename)



if __name__ == '__main__':
    pass