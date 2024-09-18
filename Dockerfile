FROM opendap/besd:3.21.0-501 AS base
HEALTHCHECK NONE

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y nano && \
    yum install -y wget

ARG HOME='/home/worker'
WORKDIR ${HOME}
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.10.0-1-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p ${HOME}/miniconda && \
    rm miniconda.sh

ENV PATH="${HOME}/miniconda/bin:${PATH}"
ARG BUILD=${HOME}/build
WORKDIR ${BUILD}

RUN pip install ipython  && \
    pip install pytest  && \
    pip install coverage

COPY setup.py requirements*txt generate_dmrpp.py ./
COPY dmrpp_generator ./dmrpp_generator/
COPY tests ./tests/
RUN pip install -r requirements.txt && \
    python setup.py install

RUN coverage run -m pytest && \
    coverage report && \
    coverage lcov -o ./coverage/lcov.info && \
    rm -rf tests .coverage .pytest_cache && \
    pip uninstall pytest -y && \
    pip uninstall coverage -y

RUN pip install --target $BUILD awslambdaric
COPY site.conf /etc/bes/
COPY bes.conf /etc/bes/

CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []
