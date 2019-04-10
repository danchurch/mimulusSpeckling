import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="makeFlowerPolygons-dcthom",
    version="0.0.27",
    author="Daniel Thomas",
    author_email="thomasdc@whitman.edu",
    description="Cooley lab tools for digitizing and analyzing Mimulus spotting patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danchurch/mimulusSpeckling",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux"
    ],
)
