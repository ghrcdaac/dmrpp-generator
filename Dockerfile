FROM opendap/besd:3.20.13-898
RUN yum -y update && \
    yum -y upgrade
HEALTHCHECK NONE
# Adding a user
RUN adduser worker
RUN yum install -y nano && \
    yum install -y wget
USER worker
WORKDIR /home/worker
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh && \
    bash Miniconda3-py38_4.8.2-Linux-x86_64.sh -b && \
    rm Miniconda3-py38_4.8.2-Linux-x86_64.sh
ENV HOME="/home/worker" PATH="/home/worker/miniconda3/bin:${PATH}"
RUN pip install ipython &&\
    pip install pytest &&\
    pip install coverage
RUN mkdir $HOME/build
ENV BUILD=$HOME/build
COPY --chown=worker setup.py requirements*txt $BUILD/
RUN pip install -r $BUILD/requirements.txt
COPY --chown=worker dmrpp_generator $BUILD/dmrpp_generator
COPY --chown=worker generate_dmrpp.py $BUILD/generate_dmrpp.py
COPY --chown=worker tests $BUILD/tests
RUN \
  cd $BUILD; \
  python setup.py install
WORKDIR $BUILD
RUN coverage run -m pytest
RUN coverage report
RUN rm -rf tests .coverage .pytest_cache
CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []
