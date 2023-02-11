
#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
#from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkSphere
)
from vtkmodules.vtkImagingCore import (
  vtkImageCast,
  vtkImageShiftScale
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)


from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

def get_program_parameters():
  import argparse
  description = 'Read a VTK image data file.'
  epilogue = ''''''
  parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('filename', help='FullHead.mhd')
  args = parser.parse_args()
  return args.filename

def main():
    iso1 = 500.0
    iso2 = 1150.0
    filename = get_program_parameters()
    reader = vtkMetaImageReader()
    reader.SetFileName(filename)
    colors = vtkNamedColors()
    mapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.AutoAdjustSampleDistancesOff()
    mapper.SetSampleDistance(0.5)
    mapper.SetBlendModeToIsoSurface()
    colorTransferFunction = vtkColorTransferFunction()
    colorTransferFunction.RemoveAllPoints()
    colorTrans2 = colors.GetColor3d("ivory")
    colorTransferFunction.AddRGBPoint(iso2,
                                     colorTrans2[0],
                                     colorTrans2[1],
                                     colorTrans2[2])
    colorTrans1 = colors.GetColor3d("flesh")
    colorTransferFunction.AddRGBPoint(iso1,
                                    colorTrans1[0],
                                    colorTrans1[1],
                                    colorTrans1[2])

    scalarOpacity = vtkPiecewiseFunction()
    scalarOpacity.AddPoint(iso1, .3)
    scalarOpacity.AddPoint(iso2, 0.6)

    volumeProperty = vtkVolumeProperty()
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(scalarOpacity)

    volume = vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)

    renderer = vtkRenderer()
    renderer.AddVolume(volume)
    renderer.SetBackground(colors.GetColor3d("cornflower"))
    renderer.ResetCamera()

    renderWindow = vtkRenderWindow()
    renderWindow.SetSize(800, 600)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName("RayCastIsosurface")

    style = vtkInteractorStyleTrackballCamera()
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.SetInteractorStyle(style)

    # Add some contour values to draw iso surfaces
    volumeProperty.GetIsoSurfaceValues().SetValue(0, iso1)
    volumeProperty.GetIsoSurfaceValues().SetValue(1, iso2)

    # Generate a good view
    aCamera = vtkCamera()
    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, -1, 0)
    aCamera.SetFocalPoint(0, 0, 0)

    renderer.SetActiveCamera(aCamera)
    renderer.ResetCamera()

    aCamera.Azimuth(30.0)
    aCamera.Elevation(30.0)
    aCamera.Dolly(1.5)
    renderer.ResetCameraClippingRange()

    renderWindow.Render()

    interactor.Start()

if __name__ == '__main__': 
    main()