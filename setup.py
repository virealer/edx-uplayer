"""Setup for edx-uplayer."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='edx-uplayer',
    version='0.1',
    author="virealer",
    author_email="virealer@gmail.com",
    description='XBlock to upload and watch video in edx',
    packages=[
        'uplayer',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'uplayer = uplayer:uplayerXBlock',
        ]
    },
    package_data=package_data("uplayer", "static"),
)
