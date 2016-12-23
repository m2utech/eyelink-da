from setuptools import setup, find_packages

from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
	long_description = f.read()

install_requires = [
    'pandas==0.19.1',
#    'scipy==0.17.0',
#    'numpy==1.11.3+mkl',
#    'scikit-learn==0.18.1',
#    'matplotlib==1.5.3',
#    'jayDeBeApi==0.2.0',
#    'jPype1==0.6.1'
    ]

setup(
    name='eyelink_python',

    version='1.0.0',

    description='Data Analyzer of eyelink for parstream',

    #url='https://github.com/eddkkang/eyelink-da',

    author='Hyeongsoo Kim',

    author_email='hyeongsoo.kim' '@' 'm2utech.com',

    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],

    keywords='eyelink data analyzer',

    packages=["DA_Lib"],

    include_package_data=True,

    install_requires=install_requires,
)
