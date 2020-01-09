import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distinctipy",
    version="1.1.4",
    author="Jack Roberts",
    author_email="jroberts@turing.ac.uk",
    description="A lightweight package for generating visually distinct colours.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alan-turing-institute/distinctipy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities"
    ],
    keywords="color colour palette colormap colorblind colourblind",
    packages=setuptools.find_packages(),
    install_requires=["matplotlib", "numpy", "pandas"]
)

