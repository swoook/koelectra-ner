FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV MECAB_KO_DIC_DIR /tmp/mecab-ko-dic-2.1.1-20180720

RUN apt-get update --fix-missing && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y build-essential git wget curl g++ default-jdk make git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -s
RUN rm $MECAB_KO_DIC_DIR/user-dic/*
COPY ./src/user-dic/ $MECAB_KO_DIC_DIR/user-dic/
WORKDIR $MECAB_KO_DIC_DIR
RUN tools/add-userdic.sh
RUN make install
    
RUN pip install --upgrade pip
RUN pip install Korpora transformers==3.3.1 seqeval fastprogress attrdict tqdm pandas pandarallel dart-fss ipywidgets matplotlib jupyterlab jupyterlab-git python-mecab-ko