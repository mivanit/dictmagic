import setuptools

from dictmagic import __version__,__description__

with open("README.md", "r", encoding="utf-8") as fr:
    long_description = fr.read()

setuptools.setup(
    name="dictmagic",
    version=__version__,
    author="mivanit",
    author_email="miv@knc.ai",
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mivanit/dictmagic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)