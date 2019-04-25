import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssxtd',
    version='0.1.9',
    packages=['ssxtd',],
    license='MIT',
    author='Xavier Godon',
    author_email='xavier.godon@protonmail.com',
    url='https://github.com/xgodon/ssxtd',
    description='semi structured xml to dict',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)