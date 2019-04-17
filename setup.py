import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssxtd',
    version='0.1.3',
    packages=['ssxtd',],
    license='MIT',
    author='Xavier Godon',
    author_email='xavier.godon@protonmail.com',
    scripts=['bin/run_exemple.py',],
    url='https://github.com/xgodon/ssxtd',
    description='Useful towel-related stuff.',
    long_description=long_description,
    install_requires=[
        "gzip",
        "zipfile",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)