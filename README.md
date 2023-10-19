# KnotTheory

This repository contains code for computing knot invariants and exploring properties of the region crossing change operation.

See KnotTheory_Presentation for a visual explanation of what the code is doing.

knots.py: Defines the Diagram class for knot diagrams with methods to compute the number of components, Gauss code, DT code, Alexander Polynomial, checkerboard shading, region vectors, diameter, and ineffective sets of a given knot diagram when initialized with the Planar Diagram code.

pd.py: Planar Diagram codes for knots with up to twelve crossings to be used to generate data.

nonalternating.py: Planar Diagram codes for nonalternating knot diagrams with eleven and twelve crossings.

links.py: Planar Diagram codes for links with up to four components and up to eleven crossings.

merge.py: Planar Diagram codes for knot diagrams with up to eight crossings merged together with one reducible crossing.

diameter.txt: Output on the diameter of reduced knot diagrams with up to twelve crossings

loop.txt: Output on the diameter of knot diagrams created by adding a reducible loop onto different segements of reduced knot diagrams.

links.txt: Output on the diameter of reduced link diagrams with up to eleven crossings.

threecomp.py: Attempts to identify patterns in the shading subsets of three-component reduced link diagrams.

fourcomp.py: Attempts to identify patterns in the shading subsets of four-component reduced link diagrams.

torus.py: Similar to knots.py but contains code to find the number of components, checkerboard shading, region vectors, and diameter of knot diagrams embedded on a torus.
