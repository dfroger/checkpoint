from setuptools import setup
from checkpoint import __version__

setup(
    name = 'checkpoint',
    version = __version__,
    url = 'https://github.com/dfroger/checkpoint',
    description = 'Checkpoints are like unit-tests inlined in your code.',
    license = 'BSD',
    author = 'David Froger',
    author_email = 'david.froger@mailoo.org',
    packages = ['checkpoint'],
    install_requires = ['h5py', 'pyyaml',]
)
