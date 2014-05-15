FROM ubuntu

RUN apt-get update

RUN apt-get install -y python python-pip wget git

RUN wget https://github.com/virtix/clouseau/archive/master.tar.gz

RUN tar xfz master.tar.gz

RUN pip install -r /clouseau-master/requirements.txt

ENV PYTHONPATH $PYTHONPATH:/clouseau-master

CMD /clouseau-master/bin/clouseau_thin -u $GIT_URL
