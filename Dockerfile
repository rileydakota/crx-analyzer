ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim-bookworm

ARG CRX_ANALYZER_VERSION
RUN pip install crx-analyzer==${CRX_ANALYZER_VERSION}

ENTRYPOINT ["crx-analyzer"]
