#!/bin/bash
echo "bash start."
python body2word.py
python tf-idf.py
python data_shaper.py
python analyzer.py
python analyzer_test.py