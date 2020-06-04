FROM ghrcdaac/hyrax:snapshot

RUN yum -y update && \
    yum -y upgrade

RUN yum install -y centos-release-scl 
# Using miniconda because rh-python is terrible
# Using a pre-downloaded Miniconda file because I am paranoid
COPY Miniconda3-latest-Linux-x86_64.sh /tmp/.
# Adding a user
RUN adduser worker
USER worker
WORKDIR /home/worker
RUN  bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b
ENV HOME="/home/worker" PATH="/home/worker/miniconda3/bin:${PATH}"

# Save some space
#RUN rm /tmp/Miniconda3-latest-Linux-x86_64.sh


RUN mkdir $HOME/build

ENV BUILD=$HOME/build 


COPY setup.py requirements*txt $BUILD/
COPY dmrpp_generator $BUILD/dmrpp_generator
COPY generate_dmrpp.py $BUILD/generate_dmrpp.py

RUN \
  cd $BUILD; \
  python setup.py install 


WORKDIR $BUILD

RUN pip install ipython

CMD ["python", "generate_dmrpp.py"]
ENTRYPOINT []


