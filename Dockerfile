FROM opendap/hyrax:snapshot

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y centos-release-scl 

COPY Miniconda3-latest-Linux-x86_64.sh .
RUN  bash Miniconda3-latest-Linux-x86_64.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"

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


