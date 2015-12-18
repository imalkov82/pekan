from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

Ages003_vtk = LegacyVTKReader( FileNames=['/home/imalkov/DropboxUni2015/M.s/Research/DATA/SESSION_TREE/NODE02/Session1B/VTK/Ages003.vtk'] )

RenderView1 = GetRenderView()
a1_ExhumationRate_PVLookupTable = GetLookupTableForArray( "ExhumationRate", 1 )

DataRepresentation2 = Show()
DataRepresentation2.EdgeColor = [0.0, 0.0, 0.5000076295109483]
DataRepresentation2.SelectionPointFieldDataArrayName = 'ExhumationRate'
DataRepresentation2.ScalarOpacityFunction = []
DataRepresentation2.ColorArrayName = ('POINT_DATA', 'ExhumationRate')
DataRepresentation2.ScalarOpacityUnitDistance = 1.495838960900772
DataRepresentation2.LookupTable = a1_ExhumationRate_PVLookupTable
DataRepresentation2.ScaleFactor = 6.000162124633789

PlotOnIntersectionCurves1 = PlotOnIntersectionCurves( SliceType="Plane" )

RenderView1.CameraClippingRange = [123.5457148353541, 138.47412023773984]

PlotOnIntersectionCurves1.SliceType.Origin = [15.01878547668457, 30.000810623168945, 32.597999572753906]

active_objects.source.SMProxy.InvokeEvent('UserEvent', 'ShowWidget')


XYChartView1 = CreateXYPlotView()

active_objects.source.SMProxy.InvokeEvent('UserEvent', 'HideWidget')


AnimationScene1 = GetAnimationScene()
DataRepresentation3 = Show()
DataRepresentation3.XArrayName = 'arc_length'
DataRepresentation3.SeriesVisibility = ['Points (0)', '0', 'Points (1)', '0', 'Points (2)', '0', 'Points (Magnitude)', '0', 'arc_length', '0', 'vtkOriginalIndices', '0']
DataRepresentation3.UseIndexForXAxis = 0

XYChartView1.BottomAxisRange = [0.0, 80.0]
XYChartView1.TopAxisRange = [0.0, 6.66]
XYChartView1.ViewTime = 0.0
XYChartView1.LeftAxisRange = [-5.0, 65.0]
XYChartView1.RightAxisRange = [0.0, 6.66]

AnimationScene1.ViewModules = [ RenderView1, XYChartView1 ]

Delete(XYChartView1)
Delete(DataRepresentation3)
AnimationScene1.ViewModules = RenderView1

active_objects.source.SMProxy.InvokeEvent('UserEvent', 'ShowWidget')


SetActiveView(RenderView1)
DataRepresentation4 = Show()
DataRepresentation4.EdgeColor = [0.0, 0.0, 0.5000076295109483]
DataRepresentation4.SelectionPointFieldDataArrayName = 'ApatiteFTAge'
DataRepresentation4.ColorArrayName = ('POINT_DATA', 'ExhumationRate')
DataRepresentation4.LookupTable = a1_ExhumationRate_PVLookupTable
DataRepresentation4.ScaleFactor = 6.000162124633789

RenderView1.CameraClippingRange = [122.17747501296641, 140.19645443192317]

Render()
