"""
Defines install behavior for the NGAC API
"""
from setuptools import setup

setup(
    name="NGAC",
    version="0.0.1",
    description="NGAC API, provides an interface for interaction with the NGAC servers",
    url="https://github.com/ivario123/NGAC_ABE",
    author="Ivar Jönsson",
    author_email="ivajns-9@student.ltu.se",
    license="MIT",
    packages=[".","ngac_types"],
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.10",
    ],
)
