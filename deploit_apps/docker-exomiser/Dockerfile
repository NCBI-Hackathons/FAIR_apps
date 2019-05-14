FROM zgmwum/exomiser

RUN apt-get update -y && apt-get install -y vim

RUN apt-get install -y unzip

RUN wget https://github.com/exomiser/Exomiser/releases/download/12.0.0/exomiser-cli-12.0.0-distribution.zip && \
	unzip exomiser-cli-12.0.0-distribution.zip && \
	rm exomiser-cli-12.0.0-distribution.zip && \
	mv /exomiser-cli-12.0.0 /exomiser

ADD application.properties /exomiser/

ADD run.py /usr/local/bin
