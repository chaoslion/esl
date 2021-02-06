FROM python:3.8-buster

ARG PACKAGE=rover*.whl

COPY dist/${PACKAGE} /tmp

RUN python3 -m pip install /tmp/${PACKAGE} && rm /tmp/${PACKAGE}

ENTRYPOINT [ "python3", "-m", "rover" ]
