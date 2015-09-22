set -e
set -x

python ml/feature_selector_test.py
python ml/learner_test.py
python ml/seti_server_test.py
python ml/run_pipeline_test.py