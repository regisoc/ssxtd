#!/bin/bash
rm -r dist/*
python3 setup.py sdist bdist_wheel --universal
python3 -m twine upload dist/*