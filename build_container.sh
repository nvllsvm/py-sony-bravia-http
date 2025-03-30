#!/usr/bin/env sh
set -ex
mkdir -p build
TAG='localhost/lounge-tv-http:latest'
OUTPUT='build/lounge-tv-http.tar.zst'
podman build --pull=always -t "$TAG" .
podman save "$TAG" | zstd > "$OUTPUT"
