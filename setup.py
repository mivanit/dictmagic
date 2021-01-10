import setuptools

with open("README.md", "r", encoding="utf-8") as fr:
    long_description = fr.read()

with open("version", "r", encoding="utf-8") as fv:
    version = fv.read().strip()

setuptools.setup(
    name="dictmagic-mivanit",
    version=version,
    author="mivanit",
    author_email="miv@knc.ai",
    description="a package that makes it easier to do weird things with python dictionaries",
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