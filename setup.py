#!/usr/bin/env python3
"""
Setup script for webpage-timelapse
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="webtimelapse",
    version="1.0.0",
    author="Stephen Giguere",
    author_email="",
    description="Capture screenshots of a webpage at intervals and create timelapse videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eurogig/webtimelapse",
    py_modules=["main"],
    scripts=["main.py"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "webtimelapse=main:main",
        ],
    },
    keywords="webpage, timelapse, screenshot, video, selenium, ffmpeg",
    project_urls={
        "Bug Reports": "https://github.com/eurogig/webtimelapse/issues",
        "Source": "https://github.com/eurogig/webtimelapse",
    },
)
