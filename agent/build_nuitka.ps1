$ErrorActionPreference = "Stop"
python -m pip install "nuitka>=2.0"
python -m nuitka --standalone --onefile --output-dir=dist agent/customsops_agent/main.py

