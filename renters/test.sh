
set -e
set -x

./ml/test.sh
python logs_to_seti_test.py