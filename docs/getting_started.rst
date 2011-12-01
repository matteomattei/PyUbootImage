.. installation:

===============
Getting Started
===============

Preferred::

 sudo pip install PyUbootImage

Alternatively::

 sudo easy_install PyUbootImage 

.. toctree::
   :maxdepth: 2

Application structure
+++++++++++++++++++++

This is a single module library in pure Python with no dependencies.

Typical use cases
+++++++++++++++++
The following code is an example on how to use the library::

 # Python imports
 import sys
 # PyUbootImage import
 import PyUbootImage

 # Read in memory the u-boot image file
 if len(sys.argv) < 2:
     sys.stdout.write('Usage: %s path_to_u-boot_image\n' % sys.argv[0])
     sys.exit(0)
 f = file(sys.argv[1],'rb')
 image_data = f.read()
 f.close()

 # Parse the header only to check the validity of the file
 image = PyUbootImage.uboot_image().fill(image_data)
 if not image.checkMagic():
     sys.stdout.write("bad magic number\n")
     sys.exit(1)

 # Fully parse the u-boot image extracting the binaries
 image = PyUbootImage.uboot_image().parse(image_data)
 sys.stdout.write("Found image \n\t", "\n\t".join( [ a[0]+":"+str(a[1]) for a in image.getInfo().items() ] ))
 i=0
 for part in image.parts:
     f = file( 'part_%02d.'+PyUbootImage.IH_COMP_EXT_LOOKUP[image.ih_comp] % i, 'wb' )
     f.write(part)
     f.close()
     i+=1
 sys.exit(0)


