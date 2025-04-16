uv build
python -m twine check dist/*
pause
uv publish
pause
python clean_pycache.py
pause