.PHONY: venv
venv:
	python3 -m venv venv

.PHONY: requirements
requirements:
	pip install -r requirements.txt
