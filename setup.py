#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import nootropic

setup(
    name='nootropic',
    version=nootropic.__version__,
    description='',
    url='https://github.com/EveripediaNetwork/nootropic',
    author='Rodrigo Martínez (brunneis)',
    author_email='dev@brunneis.com',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        '',
    ],
    package_data={
        'nootropic': [
            '',
        ],
    },
)
