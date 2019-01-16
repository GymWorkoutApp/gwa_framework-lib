# Variables
GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}
NAME := gwa-framework
BASE_DIR := ./
SRC_DIR := $(BASE_DIR)/gwa_framework/
SRC_TESTS_DIR := $(SRC_DIR)/tests/


setup:
	@echo "-- Installing Python Dependencies --"
	@pip install -r requirements.txt

setup_dev:
	@echo "-- Installing Dev Python Dependencies --"
	@pip install -r requirements-dev.txt

test:
	@echo "-- [$(NAME)] test --"
	@PYTHONPATH=$(BASE_DIR) pytest

test_watch:
	@echo "-- [$(NAME)] test watch --"
	@PYTHONPATH=$(BASE_DIR) ptw

coverage:
	@echo "-- [$(NAME)] coverage --"
	@PYTHONPATH=$(BASE_DIR) pytest --cov=$(SRC_DIR)
	@coverage-badge > static/coverage.svg

coverage_html: coverage
	@PYTHONPATH=$(BASE_DIR) pytest --cov=ecs_boleto/ --cov-report html:static/coverage_report

coverage_open: coverage_html
	@cd static/coverage_report && open http://127.0.0.1:8090/ || google-chrome http://127.0.0.1:8090/ && python3 -m http.server 8090

# Create a new release
# Usage: make release v=1.0.0
release:
	@if [ "$(v)" == "" ]; then \
		echo "You need to specify the new release version. Ex: make release v=1.0.0"; \
		exit 1; \
	fi
	@echo "Creating a new release version: ${v}"
	@echo "__version__ = '${v}'" > `pwd`/gwap_framework/version.py
	@git add gwap_framework/version.py
	@git commit -m 'New version: ${v}'
	@git tag ${v}
	@git push origin ${v}
	@git push --set-upstream origin "${GIT_CURRENT_BRANCH}"
	@git push origin