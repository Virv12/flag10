FROM rust as builder

RUN apt-get update
RUN apt-get install -y musl-tools
RUN rustup target add x86_64-unknown-linux-musl

WORKDIR /app
COPY . .
RUN RUSTFLAGS='-C target-feature=+crt-static' cargo build --release --target x86_64-unknown-linux-musl && \
	cp target/x86_64-unknown-linux-musl/release/flag10 .

FROM scratch
COPY --from=builder /app/flag10 /
CMD ["/flag10"]

