FROM fedora:rawhide

RUN dnf update -y \
  && dnf install -y \
  make \
  anaconda \
  python3-pip \
  && dnf clean all

RUN pip install \
  pylint

RUN mkdir /hello-world-anaconda-addon
WORKDIR /hello-world-anaconda-addon
