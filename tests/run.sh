pytest --strict-markers \
       --cov=biometrics_client \
       --cov-report term-missing \
       --cov-fail-under 85 \
       --mypy \
       --showlocals -vv
