This is a collection of Python scripts designed to analyse 2D images and carry out shapelet decomposition.  It depends on `numpy`, `matplotlib` and also uses `scipy.misc.factorial`

`image.py`, `shapelet.py` and `coefficients.py` define objects used by the scripts `decompose*.py`, which carry out multiple decompositions over a set of 2D images

The images are read from file in a simple ASCII format:

nx ny xmin xmax ymin ymax
(0,0) (0,1) ...  (0,ny)
.
.
.
(nx,0) (nx,1) ... (nx,ny)

(see `image.py` for details of how the code reads these files)
 
