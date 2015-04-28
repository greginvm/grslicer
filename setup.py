from distutils.core import setup
from Cython.Build import cythonize
from grslicer import VERSION

setup(
    name="GRSlicer",
    version=VERSION,
    author='Gregor Ratajc',
    author_email='me@gregorratajc.com',
    url='https://github.com/greginvm/grslicer',
    ext_modules=cythonize("grslicer/util/*.pyx")
)