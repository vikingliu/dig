rm -rf dist

# package
python3 -m build

pip3 uninstall -y dig-spider
pip3 uninstall -y scrapy
pip3 install dist/*whl

# upload
# python3 -m twine upload --repository-url  https://upload.pypi.org/legacy/ dist/*
