import mondrian

if __name__ == '__main__':
    for i in range(100):
        print('Painting #%s...' % (i))
        filename = 'mondrian%s.png' % (i)
        """width, height = 300, 300
        min_x_increase = 10
        max_x_increase = 40
        min_y_increase = 10
        max_y_increase = 40
        numPaintedRects = 20
        numDeletedSegments = 60
        scale = 8"""
        width, height = 1200, 1200
        min_x_increase = 10
        max_x_increase = 40
        min_y_increase = 10
        max_y_increase = 40
        numPaintedRects = 320
        numDeletedSegments = 800
        scale = 8
        mondrian.createMondrianArt(filename, width, height, min_x_increase, max_x_increase, min_y_increase, max_y_increase, numPaintedRects, numDeletedSegments, scale)


