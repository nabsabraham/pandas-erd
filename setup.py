import setuptools
import subprocess
import os

remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in remote_version

assert os.path.isfile("pandaserd/version.py")
with open("pandaserd/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{remote_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandaserd",
    version=remote_version,
    author="Nabila Abraham",
    author_email="nabila.abraham@gmail.com",
    description="Create ERD/data flow diagrams from pandas dataframes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nabsabraham/pandas-erd",
    packages=setuptools.find_packages(),
    package_data={"pandaserd": ["VERSION"]},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "graphviz",
    ],
)
