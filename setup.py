from os import path
from codecs import open as codopen
from importlib import import_module
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

__version__ = import_module('dmrpp_generator.version').__version__


# get dependencies

with codopen(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]


setup(
    name='dmrpp_file_generator',
    version=__version__,
    author='Abdelhak Marouane (am0089@uah.edu)',
    description='Library to generate DMRpp files from netCDF and HDF files, can be used with ECS activity',
    url='https://github.com/ghrcdaac/dmrpp-generator',
    license='Apache 2.0',
    classifiers=[
        'Framework :: Pytest',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Freeware',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'dmrpp-generator=dmrpp_generator.main:DMRPPGenerator.cli',
            'generate-validate-dmrpp=dmrpp_generator.generate_and_validate_dmrpp:main'
            ]
    },
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
)
