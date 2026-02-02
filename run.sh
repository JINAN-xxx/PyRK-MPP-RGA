#!/bin/bash
BASE_DIR=$(cd "$(dirname "$0")"; pwd)

# 强制优先使用 release/lib 下的库，而不是系统的
export LD_LIBRARY_PATH=$BASE_DIR/lib:$BASE_DIR:$LD_LIBRARY_PATH

echo "running demo..."
python3 demo.py
