FROM opendap/besd:3.21.1-400 AS base
HEALTHCHECK NONE

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y nano && \
    yum install -y wget && \
    yum install -y gcc

ARG HOME='/home/worker'
WORKDIR ${HOME}
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py312_25.9.1-3-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p ${HOME}/miniconda && \
    rm miniconda.sh

ENV PATH="${HOME}/miniconda/bin:${PATH}"
ARG BUILD=${HOME}/build
WORKDIR ${BUILD}

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install ipython  && \
    pip install pytest  && \
    pip install coverage

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./dmrpp_generator/ ./dmrpp_generator/
COPY ./setup.py ./
COPY generate_dmrpp.py .
RUN python setup.py install

COPY tests ./tests/
RUN coverage run -m pytest && \
   coverage report -m && \
   coverage lcov -o ./coverage/lcov.info && \
   rm -rf tests .coverage .pytest_cache && \
   pip uninstall pytest -y && \
   pip uninstall coverage -y

RUN pip install --target $BUILD awslambdaric
COPY site.conf /etc/bes/
COPY bes.conf /etc/bes/

CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []
