#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='PyUbootImage',
    version='0.3',
    description='Uboot image parser',
    long_description='This package provides a way to read u-boot images header and to retrieve encapsulated binaries. It also handles multi-image files.',
    author='Matteo Mattei; Nicola Ponzeveroni; Roberto Celeste',
    author_email='info@matteomattei.com; nicola.ponzeveroni@gilbarco.com; roberto.celeste@gmail.com',
    url='https://github.com/matteomattei/PyUbootImage',
    packages=find_packages(),
    keywords=["filesystem", "parser", "u-boot"],
    install_requires=[
        "enum34;python_version<'3.4'",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
