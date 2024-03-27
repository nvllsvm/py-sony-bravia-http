FROM python
COPY . /src
RUN pip install /src \
 && mv /src/bin/sony-bravia-cli /usr/local/bin/sony-bravia-cli
ENTRYPOINT ["/usr/local/bin/lounge-tv-http"]
