default: pylint pytest

pylint:
    find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
    PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn backend_summeu.api.fast:app --reload
reinstall_package:
	@pip uninstall -y backend_summeu || :
	@pip install -e .
# 
