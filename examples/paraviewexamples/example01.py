__author__ = 'imalkov'

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

Ages003_vtk = LegacyVTKReader( FileNames=['/home/imalkov/DropboxUni2015/M.s/Research/DATA/SESSION_TREE/NODE02/Session1B/VTK/Ages003.vtk'] )

RenderView1 = GetRenderView()
a1_ExhumationRate_PVLookupTable = GetLookupTableForArray( "ExhumationRate", 1, RGBPoints=[-0.17974573373794556, 0.23, 0.299, 0.754, 0.09314573556184769, 0.706, 0.016, 0.15], VectorMode='Magnitude', NanColor=[0.25, 0.0, 0.0], ColorSpace='Diverging', ScalarRangeInitialized=1.0, AllowDuplicateScalars=1 )

a1_ExhumationRate_PiecewiseFunction = CreatePiecewiseFunction( Points=[0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0] )

DataRepresentation1 = Show()
DataRepresentation1.EdgeColor = [0.0, 0.0, 0.5000076295109483]
DataRepresentation1.SelectionPointFieldDataArrayName = 'ExhumationRate'
DataRepresentation1.ScalarOpacityFunction = a1_ExhumationRate_PiecewiseFunction
DataRepresentation1.ColorArrayName = ('POINT_DATA', 'ExhumationRate')
DataRepresentation1.ScalarOpacityUnitDistance = 1.495838960900772
DataRepresentation1.LookupTable = a1_ExhumationRate_PVLookupTable
DataRepresentation1.ScaleFactor = 6.000162124633789

RenderView1.CenterOfRotation = [15.01878547668457, 30.000810623168945, 32.597999572753906]

a1_ExhumationRate_PVLookupTable.ScalarOpacityFunction = a1_ExhumationRate_PiecewiseFunction

RenderView1.CameraPosition = [15.01878547668457, 30.000810623168945, 162.61389248703105]
RenderView1.CameraFocalPoint = [15.01878547668457, 30.000810623168945, 32.597999572753906]
RenderView1.CameraClippingRange = [123.5457148353541, 138.47412023773984]
RenderView1.CameraParallelScale = 33.650589252224805

Render()
