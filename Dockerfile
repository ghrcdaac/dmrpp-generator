FROM opendap/besd:3.21.0-272
RUN yum -y update && \
    yum -y upgrade
HEALTHCHECK NONE
RUN yum install -y nano && \
    yum install -y wget
# Adding a user
RUN adduser worker
USER worker
WORKDIR /home/worker
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.10.0-1-Linux-x86_64.sh && \
    bash Miniconda3-py310_23.10.0-1-Linux-x86_64.sh -b && \
    rm Miniconda3-py310_23.10.0-1-Linux-x86_64.sh
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
RUN coverage lcov -o ./coverage/lcov.info
RUN rm -rf tests .coverage .pytest_cache
CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []
