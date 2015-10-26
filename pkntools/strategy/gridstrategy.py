__author__ = 'imalkov'
import numpy

class EscarpmentGrid:
    def __init__(self, colnum, rownum, context):
        self.context = context
        self.xsize = int(rownum)
        self.ysize = int(colnum)

    def make_footwall(self, maxh):
        '''
        Create footwall grid
        :param maxh:
        :return:
        '''
        footwall_maxh = maxh * numpy.sin(numpy.deg2rad(self.context.velangle))
        xi,yi = numpy.mgrid[0:self.xsize , 0:self.ysize / 2]
        esc_init_grid = yi * self.context.yscale * numpy.tan(numpy.deg2rad(self.context.escangle))
        esc_init_grid[esc_init_grid > footwall_maxh] = footwall_maxh #fit footwall to maximum height
        return esc_init_grid

    def makegrid(self, maxh):
        footwall_grid = self.make_footwall(maxh)
        res_grid = numpy.concatenate((numpy.zeros(footwall_grid.shape), footwall_grid), axis=1)
        return res_grid.transpose().flatten()


class PlatoGrid(EscarpmentGrid):
    def __init__(self, colnum, rownum, context):
        EscarpmentGrid.__init__(self, colnum, rownum, context)


class CanyonGrid(EscarpmentGrid):
    def __init__(self, colnum, rownum, context):
        EscarpmentGrid.__init__(self, colnum, rownum, context)

    def make_footwall(self, maxh):
        xi,yi = numpy.mgrid[0:numpy.ceil(self.xsize / 2.0), 0:numpy.ceil(self.ysize / 2.0)]
        cyn_left_init_grid = xi * self.context.xscale * numpy.tan(numpy.deg2rad(self.context.cnynangle))
        cyn_grid = numpy.concatenate((numpy.flipud(cyn_left_init_grid[self.xsize%2:]),cyn_left_init_grid),axis=0)
        # escarpment
        esc_grid = EscarpmentGrid.make_footwall(self, maxh)
        # final topography
        esc_grid[cyn_grid < esc_grid] = cyn_grid[cyn_grid < esc_grid]
        return esc_grid
