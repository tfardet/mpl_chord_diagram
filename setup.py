from setuptools import setup, find_packages


# Get version information, recommended here
# https://packaging.python.org/guides/single-sourcing-package-version
info = {}

with open("_info.py") as fp:
    exec(fp.read(), info)


# Package information and setup instructions
long_descr = '''
The module enables to plot chord diagrams with matplotlib from lists,
numpy or scipy sparse matrices.
It provides tunable parameters such as arc sorting based on size or distance,
and supports gradients to better visualize source and target regions.
'''

setup(
    name='mpl_chord_diagram',
    version=info['__version__'],
    description='Python module to plot chord diagrams with matplotlib.',
    package_dir={'mpl_chord_diagram': '.'},
    packages=['mpl_chord_diagram'],

    # Include the non python files:
    package_data={'': ['LICENSE', '*.md']},

    # Requirements
    install_requires=['numpy', 'scipy', 'matplotlib'],

    # Metadata
    url='https://codeberg.org/tfardet/mpl_chord_diagram',
    author=info['__author__'],
    author_email=info['__email__'],
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
