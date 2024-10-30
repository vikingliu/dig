# package
python3 -m build

# upload
python3 -m twine upload --repository-url  https://upload.pypi.org/legacy/ dist/*