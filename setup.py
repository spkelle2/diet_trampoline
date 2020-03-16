import setuptools
import diet
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diet",
    version=diet.__version__,
    author="Sean",
    description="The Diet Problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spkelle2/diet",
    packages=['diet', 'test_diet'],
    install_requires=[
        'ticdat',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)