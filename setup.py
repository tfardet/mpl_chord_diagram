import os, errno
from setuptools import setup, find_packages
from shutil import rmtree, copy2


# create mpl_chord_diagram directory and move important files
setup_dir = os.path.abspath(os.path.dirname(__file__))
directory = os.path.join(setup_dir, 'mpl_chord_diagram')

move = (
    '__init__.py',
    '_info.py',
    'LICENSE',
    'chord_diagram.py',
    'gradient.py',
    'utilities.py',
    'example.py',
)


# Layout changes between git repo (flat) and Pypi (hierarchical) so check if
# flat layout files exist. If not, then all files are already in the subfolder

dir_preexists = False

if not os.path.exists(directory):
    os.makedirs(directory)

    for fname in move:
        copy2(fname, directory)
else:
    dir_preexists = True


# Get version information, recommended here
# https://packaging.python.org/guides/single-sourcing-package-version
info = {}

with open(os.path.join(directory, "_info.py")) as fp:
    exec(fp.read(), info)


# Package information and setup instructions
long_descr = '''
The module enables to plot chord diagrams with matplotlib from lists,
numpy or scipy sparse matrices.
It provides tunable parameters such as arc sorting based on size or distance,
and supports gradients to better visualize source and target regions.
'''

try:
    setup(
        name='mpl_chord_diagram',
        version=info['__version__'],
        description='Python module to plot chord diagrams with matplotlib.',
        package_dir={'': '.'},
        packages=find_packages('.'),

        # Include the non python files:
        package_data={'': ['LICENSE', '*.md']},

        # Requirements
        install_requires=['numpy', 'scipy', 'matplotlib'],

        # Metadata
        url='https://codeberg.org/tfardet/mpl_chord_diagram',
        author='Tanguy Fardet',
        author_email='tanguy.fardet@tuebingen.mpg.de',
        license='MIT',
        keywords='chord diagram matplotlib plotting',
        long_description=long_descr,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Visualization',
            'Framework :: Matplotlib',
        ]
    )
finally:
    # only useful for package generation from git repo
    if not dir_preexists:
        rmtree(directory, ignore_errors=True)
