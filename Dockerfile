ARG IMAGE=python:3.13-slim

FROM $IMAGE AS build
RUN apt-get update \
 && apt-get install -y git
RUN pip install hatch
COPY . /src
WORKDIR /src
RUN hatch build -t wheel

FROM $IMAGE
COPY --from=build /src/dist/*.whl /dist/
RUN pip install /dist/*whl
COPY bin/sony-bravia-cli /usr/local/bin/sony-bravia-cli
ENTRYPOINT ["/usr/local/bin/lounge-tv-http"]
