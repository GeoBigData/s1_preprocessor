FROM continuumio/miniconda:latest

# create the conda environment
RUN mkdir /helper
COPY ./environment.yml /helper
RUN conda env create -f /helper/environment.yml

# get SNAP executables
RUN cd /helper && wget http://step.esa.int/downloads/6.0/installers/esa-snap_sentinel_unix_6_0.sh
# install SNAP execexutables
RUN yes "" | bash /helper/esa-snap_sentinel_unix_6_0.sh
# set memory max to 16 GB
RUN sed -i -e 's/-Xmx1G/-Xmx16G/g' /opt/snap/bin/gpt.vmoptions

# install zip CLI
RUN apt-get install zip -y

# move the scripts over
ADD . /s1_preprocessor
SHELL ["/bin/bash", "-c"]
RUN echo "source activate s1_preprocessor" > ~/.bashrc
ENV PATH /opt/conda/envs/s1_preprocessor/bin:$PATH
ENV PATH /opt/conda/envs/s1_preprocessor/bin:$PATH
RUN cd /s1_preprocessor && python setup.py install

ENV PYTHONPATH /s1_preprocessor









