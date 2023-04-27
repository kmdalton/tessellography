from setuptools import setup, find_packages

# Get version number
def getVersionNumber():
    with open("tessellography/VERSION", "r") as vfile:
        version = vfile.read().strip()
    return version


__version__ = getVersionNumber()

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/kmdalton/tessellography/issues",
    "Source Code": "https://github.com/kmdalton/tessellography",
}


LONG_DESCRIPTION = """
A simple library of 2d crystallography objects for teaching crystallography
"""

setup(
    name="tessellography",
    version=__version__,
    author="Kevin M. Dalton",
    author_email="kmdalton@fas.harvard.edu",
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    description="2d crystallography for teachers",
    project_urls=PROJECT_URLS,
    python_requires=">=3.8,<3.11",
    url="https://github.com/kmdalton/tessellography",
    install_requires=[
        "tqdm",
        "matplotlib",
        "seaborn",
        "numpy",
        "scipy",
        "scikit-learn",
        "mpl-arrow",
    ],
    scripts=[
    ],
    entry_points={
        "console_scripts": [
        ]
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
)
