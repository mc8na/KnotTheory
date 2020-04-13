# KnotTheory

This repository contains code for computing knot invariants and exploring properties of the region crossing change operation. 

knots.py: Defines the Diagram class for knot diagrams with methods to compute the number of components, Gauss code, DT code, Alexander Polynomial, checkerboard shading, region vectors, diameter, and ineffective sets of a given knot diagram when initialized with the Planar Diagram code.

pd.py: Planar Diagram codes for knots with up to twelve crossings to be used to generate data.

nonalternating.py: Planar Diagram codes for nonalternating knot diagrams with eleven and twelve crossings.

merge.py: Planar Diagram codes for knot diagrams with up to eight crossings merged together with one reducible crossing.

diameter.txt: Output on the diameter of reduced knot diagrams with up to twelve crossings

loop.txt: Output on the diameter of knot diagrams created by merging two reduced diagrams together with one reducible crossing.

links.txt: Output on the diameter of reduced link diagrams with up to eleven crossings.

threecomp.py: Attempts to identify patters in the shading subsets of three-component reduced link diagrams.

fourcomp.py: Attempts to identify patterns in the shading subsets of four-component reduced link diagrams.

torus.py: Similar to knots.py but contains code to find the number of components, checkerboard shading, region vectors, and diameter of knot diagrams embedded on a torus.
