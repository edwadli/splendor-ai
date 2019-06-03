find . -name '*.pyc' -delete
python -m unittest discover -s . -p "*_test.py"
