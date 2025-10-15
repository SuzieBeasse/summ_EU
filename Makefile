default: pylint pytest

pylint:
    find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
    PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn backend_summeu.api.fast:app --reload
reinstall_package:
	@pip uninstall -y backend_summeu || :make
	@pip install -e backend_summeu
#

docker_build_local:
	docker build --tag=$(GAR_IMAGE):dev .

docker_run_local:
	docker run \
		-e PORT=8000 -p 8000:8000 \
		--env-file .env \
		$(GAR_IMAGE):dev

docker_run_local_interactively:
	docker run -it \
		-e PORT=8000 -p 8000:8000 \
		--env-file .env \
		$(GAR_IMAGE):dev \
		bash
