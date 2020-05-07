FROM opendap/hyrax:snapshot

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y centos-release-scl 
# Using miniconda because rh-python is terrible
# Using a pre-downloaded Miniconda file because I am paranoid
COPY Miniconda3-latest-Linux-x86_64.sh .
RUN  bash Miniconda3-latest-Linux-x86_64.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"
# Save some space
RUN rm Miniconda3-latest-Linux-x86_64.sh
COPY config/dmrpp.conf dmrpp.conf

RUN mkdir /build

ENV BUILD=/build 


COPY setup.py requirements*txt $BUILD/
COPY dmrpp_generator $BUILD/dmrpp_generator

RUN \
  cd $BUILD; \
  python setup.py install 


WORKDIR $BUILD

ENTRYPOINT []


