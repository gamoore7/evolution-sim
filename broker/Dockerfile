FROM rust:1.67 as builder
WORKDIR /usr/src/broker
COPY . .
RUN cargo install --path .

FROM debian:buster-slim
RUN apt-get update
RUN apt-get install -y #extra-runtime-dependencies
RUN rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/cargo/bin/broker /usr/local/bin/broker
EXPOSE 8000
CMD ["broker"]
