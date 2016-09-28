#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='python_image_clone_detection',
    version='0.0.1',
    description="Python package to detect if an image has duplicate 'copy-and-paste' (clone) images in it.",
    long_description=readme + '\n\n' + history,
    author="Shane Devane",
    author_email='shanedevane@gmail.com',
    url='https://github.com/shanedevane/python_image_clone_detection',
    packages=[
        'python_image_clone_detection',
    ],
    package_dir={'python_image_clone_detection':
                 'python_image_clone_detection'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='python_image_clone_detection',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
