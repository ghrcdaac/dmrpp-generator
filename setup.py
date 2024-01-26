from os import path
from codecs import open as codopen
from setuptools import setup, find_packages
from dmrpp_generator import version


# get dependencies
with codopen(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]


setup(
    name='dmrpp_generator',
    version=version.__version__,
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
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'dmrpp-process=dmrpp_generator.main:DMRPPGenerator.cli',
            'dmrpp=dmrpp_generator.generate_and_validate_dmrpp:main'
            ]
    },
    packages=find_packages(exclude=['docs', 'tests*']),
    package_data={"dmrpp_generator": ["*.yml"]},
    include_package_data=True,
    install_requires=install_requires,
)
