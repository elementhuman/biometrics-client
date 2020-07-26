pytest --strict-markers \
       --cov=biometrics_client \
       --cov-report term-missing \
       --cov-fail-under 80 \
       --mypy \
       --showlocals -vv
