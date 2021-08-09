import os, errno
from setuptools import setup, find_packages
from shutil import rmtree, copy2


# create directory
setup_dir = os.path.abspath(os.path.dirname(__file__))
directory = os.path.join(setup_dir, 'mpl_chord_diagram')

try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


# move important files
move = (
    '__init__.py',
    '_info.py',
    'LICENSE',
    'chord_diagram.py',
    'gradient.py',
    'utilities.py',
    'example.py',
)


for fname in move:
    copy2(fname, directory)

long_descr = '''
The module enables to plot chord diagrams with matplotlib from lists,
numpy or scipy sparse matrices.
It provides tunable parameters such as arc sorting based on size or distance,
and supports gradients to better visualize source and target regions.
'''

# Recommended here https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
info = {}
with open("_info.py") as fp:
    exec(fp.read(), info)

# install
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

rmtree(directory, ignore_errors=True)
