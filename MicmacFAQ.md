# Micmac 101
Quick Explanation of Micmac basic commands used for the 3D reconstruction of ludox experiments.


### The command line
Micmac is a command line software, meaning it has no graphical interface to interact with. Instead, we call Micmac through a command line prompt (or Terminal) with the command 
>`mm3d`

### mm3d commands syntax
All micmac calls have the same general expression 
>`mm3d Function Arguments`

The next paragraphs aim to describe these different "Functions", their utility and the "Arguments" to pass them.

### Tapioca : tie points search
Exemple:
>`mm3d Tapioca All ".*JPG" -1`

Compute the tie points common to selected images.
Tie points are small windows of pixels with a high brightness gradient that can be seen on
multiple images.

Arguments: 
  - All &rarr; find tie points between ALL images
  - -1 &rarr; resolution (-1 means max res)


### Tapas/Apero? : relative camera positions
Exemple:
>`'mm3d Tapas FraserBasic ".*JPG" Out=MyFolder'`

Knowing the cameras internal parameters, and the position of tie points on each images, the
command Apero (or Tapas ?) computes the cameras positions and orientations for each image relative to an
arbitrary system.

Arguments: 
  - FraserBasic &rarr; method to use (more complex methods often don't converge)
  - Out=MyFolder &rarr; where to save the output
 
### Apericloud : first order point cloud
>`mm3d AperiCloud ".*JPG" MyFolder`

Creates a first attempt at generating a point cloud. Most of time, the generated point cloud is not good at all at this step. However after GeoImage it will be much better.

### Malt GeoImage: Digital Elevation Model
> `mm3d Malt GeomImage ".*JPG" MyFolder Master=image1.JPG ZoomF=2`

Micmac generates a depth map in the region delimited by the
master image mask.

Arguments: 
  - MyFolder &rarr; where input and output will be located
  - Master=image1.JPG &rarr; which image is chosen as reference (for example to color the point cloud)
  - ZoomF &rarr; Zoom factor (ie resolution of the point cloud. /!\ if ZoomF too small (1 for exemple) then convergence is not guaranted. Choose 4 or 8 first then reduce.

### NUage2Ply: Point cloud generation
>`mm3d Nuage2Ply "MM-Malt-Img-image1/NuageImProf_STD-MALT_Etape_4.xml" Attr="image1.JPG" Out=nuage.ply RatioAttrCarte=2`

Arguments: 
-  RatioAttrCarte=2 &rarr; should be the same as ZoomF
-  Out=nuage.ply &rarr; output file containing the point cloud
