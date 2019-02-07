import mondrian

if __name__ == '__main__':
    for i in range(100):
        print('Painting #%s...' % (i))
        filename = 'mondrian%s.png' % (i)
        width, height = 400, 400
        min_x_increase = 15
        max_x_increase = 70
        min_y_increase = 15
        max_y_increase = 70
        numPaintedRects = 16
        numDeletedSegments = 40
        mondrian.createMondrianArt(filename, width, height, min_x_increase, max_x_increase, min_y_increase, max_y_increase, numPaintedRects, numDeletedSegments)


