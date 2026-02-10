FROM opendap/besd:3.21.1-896 AS base
HEALTHCHECK NONE

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y nano && \
    yum install -y wget && \
    yum install -y gcc

ARG UV_VERSION='0.10.0'
ARG HOME='/home/worker'
WORKDIR ${HOME}

ADD https://astral.sh/uv/${UV_VERSION}/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="${HOME}/.local/bin/:$PATH"

ARG BUILD=${HOME}/build
WORKDIR ${BUILD}

COPY pyproject.toml uv.lock ./
COPY ./src ./src
COPY ./tests ./tests
COPY site.conf /etc/bes/
COPY bes.conf /etc/bes/

RUN uv sync --all-groups
ENV PATH="${BUILD}/.venv/bin:$PATH"

RUN uv run pytest
CMD ["python", "./src/generate_dmrpp.py"]
ENTRYPOINT []
