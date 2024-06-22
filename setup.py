import os.path

from setuptools import find_packages, setup


def source_root_dir():
    """Return the path to the root of the source distribution."""
    return os.path.abspath(os.path.dirname(__file__))


def read_long_description():
    """Read from the README file in root of source directory."""
    readme = os.path.join(source_root_dir(), "README.md")
    with open(readme) as fin:
        return fin.read()

setup(
    name="jw.py",
    description="The command line interface to Faculty",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/deese/justwatch-cli",
    author="Javier DeeSe",
    author_email="deese2k@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
    install_requires=[
        'rich',
        "simple-justwatch-python-api",
        "cinemagoer"
    ],
    scripts=['justwatch-cli/jw.py'],
)
