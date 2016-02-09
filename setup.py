from setuptools import setup
from clash import __version__

setup(
    name = 'clash',
    version = __version__,
    url = 'https://github.com/thni/clash',
    description = 'Store Python Class data members in HDF5 files',
    license = 'BSD',
    author = 'David Froger',
    author_email = 'david.froger@mailoo.org',
    packages = ['clash'],
    install_requires = ['h5py', 'pyyaml',]
)
