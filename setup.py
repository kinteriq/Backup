import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="backup-kinteriq",
    version="0.0.1",
    author="kinteriq",
    author_email="kinteriq@gmail.com",
    description="A tool for backups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kinteriq/Backup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
)
