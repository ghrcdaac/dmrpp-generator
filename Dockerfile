ARG HOME='/home/worker'
ARG BUILD=${HOME}/build

FROM opendap/besd:3.21.0-272 AS base
HEALTHCHECK NONE

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y nano && \
    yum install -y wget

ARG HOME
WORKDIR $HOME
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.10.0-1-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p ${HOME}/miniconda && \
    rm miniconda.sh && \
    source ${HOME}/miniconda/bin/activate && \
    conda init --all
ENV PATH="${HOME}/miniconda/bin:${PATH}"

ARG BUILD
WORKDIR ${BUILD}

COPY setup.py requirements*txt ./
RUN pip install -r requirements.txt
COPY dmrpp_generator ./dmrpp_generator
COPY generate_dmrpp.py ./generate_dmrpp.py
COPY tests ./tests

RUN python setup.py install

RUN pip install ipython  && \
    pip install pytest  && \
    pip install coverage
RUN coverage run -m pytest
RUN coverage report
RUN coverage lcov -o ./coverage/lcov.info
RUN rm -rf tests .coverage .pytest_cache

ARG BUILD
RUN pip install --target $BUILD awslambdaric
COPY site.conf /etc/bes/

CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []
