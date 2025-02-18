python -m build
python -m twine check dist/*
pause
python -m twine upload dist/* --verbose
pause
python clean_pycache.py
pause