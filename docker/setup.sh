#!/bin/sh
set -xe

cd "$(realpath "$(dirname "$0")")/.."

RUSTFLAGS='-C target-feature=+crt-static' cargo build --release --target x86_64-unknown-linux-musl

cp target/x86_64-unknown-linux-musl/release/flag10 .token docker
pushd docker
docker build --no-cache -t flag10 .
popd
