
set -e
set -x

./ml/test.sh
python feature_extractor_test.py
python logs_to_seti_test.py
python renters_serving_scorer_test.py