del /f /q .\dist\*.*

python setup.py sdist

python setup.py bdist_wheel

twine upload dist/*

pip.exe install --upgrade e_drone
