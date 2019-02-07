# Mondrian Art Generator, by Al Sweigart al@inventwithpython.com
# Randomly generates PNG images of Mondrian-style art.

# This program requires Pillow, install it with `pip install pillow`

__version__ = '0.0.1'

import random
import logging
logging.basicConfig(filename='mondrian_log.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')

WHITE = 0
BLACK = 1
RED = 2
YELLOW = 3
BLUE = 4
COLOR_MAPPING = {WHITE: 'white', BLACK: 'black', RED: 'red', YELLOW: 'yellow', BLUE: 'blue'}

def createMondrianArt():
    imageNumber = 0
    logging.debug('Starting painting #%s' % (imageNumber))
    WIDTH, HEIGHT = 200, 200
    MIN_X_INCREASE = 15
    MAX_X_INCREASE = 45
    MIN_Y_INCREASE = 15
    MAX_Y_INCREASE = 45

    numberOfRectanglesToPaint = 12
    numberOfSegmentsToDelete = 600

    logging.debug('WIDTH, HEIGHT = %s, %s' % (WIDTH, HEIGHT))
    logging.debug('MIN_X_INCREASE, MAX_X_INCREASE = %s, %s' % (MIN_X_INCREASE, MAX_X_INCREASE))
    logging.debug('MIN_Y_INCREASE, MAX_Y_INCREASE = %s, %s' % (MIN_Y_INCREASE, MAX_Y_INCREASE))

    print('Image #%s, %sx%s' % (imageNumber, WIDTH, HEIGHT))

    # Pre-populate the board with blank spaces:
    board = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board[(x, y)] = WHITE

    # Generate vertical lines:
    numberOfLines = 0
    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    while x < WIDTH - MIN_X_INCREASE:
        numberOfLines += 1
        for y in range(HEIGHT):
            board[(x, y)] = BLACK
        x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)

    # Generate horizontal lines:
    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    while y < HEIGHT - MIN_Y_INCREASE:
        numberOfLines += 1
        for x in range(WIDTH):
            board[(x, y)] = BLACK
        y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    logging.debug('numberOfRectanglesToPaint = %s' % (numberOfRectanglesToPaint))
    logging.debug('numberOfSegmentsToDelete  = %s' % (numberOfSegmentsToDelete))

    # Randomly select points and try to remove them.
    segmentDeleteAttempts = 0
    print('    Deleting up to %s segments...' % (numberOfSegmentsToDelete))
    for i in range(numberOfSegmentsToDelete):
        while True:
            breakAgain = False
            segmentDeleteAttempts += 1
            if segmentDeleteAttempts == numberOfSegmentsToDelete:
                breakAgain = True
                break # It's too hard to find a deleteable segment, so stop trying.

            # Get a random start point on an existing segment:
            startx = random.randint(1, WIDTH - 2)
            starty = random.randint(1, HEIGHT - 2)
            if board[(startx, starty)] == WHITE:
                continue

            # Find out if we're on a vertical or horizontal segment:
            if board[(startx - 1, starty)] == board[(startx + 1, starty)] == WHITE:
                orientation = 'vertical'
            elif board[(startx, starty - 1)] == board[(startx, starty + 1)] == WHITE:
                orientation = 'horizontal'
            else:
                # The start point is on an intersection, so get a new random start point:
                continue

            pointsToDelete = [(startx, starty)]

            canDeleteSegment = True
            if orientation == 'vertical':
                # Go up one path from the start point, and see if we can remove this segment:
                for changey in (-1, 1):
                    y = starty
                    while 0 < y < HEIGHT - 1:
                        y += changey
                        if board[(startx - 1, y)] == board[(startx + 1, y)] == BLACK:
                            # We've found a four-way intersection.
                            break
                        elif ((board[(startx - 1, y)] == WHITE and
                               board[(startx + 1, y)] == BLACK) or
                              (board[(startx - 1, y)] == BLACK and
                               board[(startx + 1, y)] == WHITE)):
                            # We've found a T-intersection; we can't delete this segment:
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((startx, y))

            elif orientation == 'horizontal':
                # Go up one path from the start point, and see if we can remove this segment:
                for changex in (-1, 1):
                    x = startx
                    while 0 < x < WIDTH - 1:
                        x += changex
                        if board[(x, starty - 1)] == board[(x, starty + 1)] == BLACK:
                            # We've found a four-way intersection.
                            break
                        elif ((board[(x, starty - 1)] == WHITE and
                               board[(x, starty + 1)] == BLACK) or
                              (board[(x, starty - 1)] == BLACK and
                               board[(x, starty + 1)] == WHITE)):
                            # We've found a T-intersection; we can't delete this segment:
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((x, starty))
            if not canDeleteSegment:
                continue # Get a new random start point.
            break # Move on to delete the segment.
        if breakAgain:
            break

        # If we can delete this segment, set all the points to white:
        for x, y in pointsToDelete:
            board[(x, y)] = WHITE

    # Add the border lines:
    for x in range(WIDTH):
        board[(x, 0)] = BLACK # Top border.
        board[(x, HEIGHT - 1)] = BLACK # Bottom border.
    for y in range(HEIGHT):
        board[(0, y)] = BLACK # Left border.
        board[(WIDTH - 1, y)] = BLACK # Right border.

    # Paint the rectangles:
    rectanglePaintAttempts = 0
    print('    Painting up to %s rectangles...' % (numberOfRectanglesToPaint))
    #input()
    for i in range(numberOfRectanglesToPaint):
        while True:
            breakAgain = False
            rectanglePaintAttempts += 1
            #print(rectanglePaintAttempts)
            if rectanglePaintAttempts == numberOfRectanglesToPaint:
                breakAgain = True
                break # It's too hard to find a paintable rectangle, so stop trying.

            startx = random.randint(1, WIDTH - 2)
            starty = random.randint(1, HEIGHT - 2)

            if board[(startx, starty)] != WHITE:
                continue # Get a new random start point.
            else:
                break

        if breakAgain:
            break

        # Flood fill algorithm:
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([(startx, starty)])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            board[(x, y)] = colorToPaint
            if board[(x - 1, y)] == WHITE:
                pointsToPaint.add((x - 1, y))
            if board[(x + 1, y)] == WHITE:
                pointsToPaint.add((x + 1, y))
            if board[(x, y - 1)] == WHITE:
                pointsToPaint.add((x, y - 1))
            if board[(x, y + 1)] == WHITE:
                pointsToPaint.add((x, y + 1))

    # Draw the board data structure:
    print('    Writing data to image...')
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(im)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            draw.point((x, y), COLOR_MAPPING[board[(x, y)]])

    im = im.resize((WIDTH * 4, HEIGHT * 4))
    im.save('mondrian%s.png' % (imageNumber))



if __name__ == '__main__':
    pass