# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    
    name='python-selve',  # Required    
    version='1.3.1',  # Required  
    description='Python library for interfacing with selve devices using the USB-RF controller',  # Required   
    long_description=long_description,  # Optional    
    url='https://github.com/gpulido/python-selve',  # Optional
    author='Gabriel Pulido',  # Optional
   
    author_email='gabriel.pulidodetorres@gmail.com',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional        
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
   
    keywords='selve blind awning shutter usb rf',  # Optional

    packages=["selve"],  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'pySerial',
        'pybase64',
        'untangle'
        ],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
           # 'sample=sample:main',
        ],
    },
)


# [metadata]
# name = python-selve
# version = 1.3.0
# description = 'Python library for interfacing with selve devices using the USB-RF controller',  # Required   
# long_description = file: README.rst
# keywords = selve, blind, awning, shutter, usb, rf
# license = MIT
# license_file = LICENSE

# home-page  = https://github.com/gpulido/python-selve
# author = Gabriel Pulido

# author_email = gabriel.pulidodetorres@gmail.com

# classifiers =    
#     Development Status :: 3 - Alpha
#     Intended Audience :: Developers
#     Topic :: Software Development :: Build Tools
#     License :: OSI Approved :: MIT License
#     Programming Language :: Python :: 3
#     Programming Language :: Python :: 3.4
#     Programming Language :: Python :: 3.5
#     Programming Language :: Python :: 3.6
#     Programming Language :: Python :: 3.7
#     Programming Language :: Python :: 3.8
#     Programming Language :: Python :: 3.9

# [options]
# packages = find:

# install_requires = 
#     pySerial
#     pybase64
#     untangle
# scripts =
#     cli/selve_cli.py

# # setup_requires =
# #   setuptools_scm