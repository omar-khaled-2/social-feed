FROM rust:1.90-slim


WORKDIR /usr/src/app


COPY Cargo.toml ./

COPY src ./src

RUN cargo build --release

ENTRYPOINT ["./target/release/jwt-generator"]


