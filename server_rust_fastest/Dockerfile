# step 1
FROM tensorflow/tensorflow:devel as library_builder2
# build tflite shared library with cmake, as per documentation (https://www.tensorflow.org/lite/guide/build_cmake)
RUN apt-get update && apt-get install --yes cmake
RUN mkdir tflite_build
ENV TFLITEC_BAZEL_COPTS="-march=native"
RUN cd tflite_build && cmake ../tensorflow_src/tensorflow/lite/c
# make sure to limit the number of parallel builds to not consume infinite memory, I use 20
RUN cd tflite_build && cmake --build . -j 20
# /tlite_build/libtensorflowlite_c.so should be created


# step 2
FROM ubuntu as application_builder
# install rust nightly to support rust-rocket
RUN apt-get update && apt-get install --yes curl gpg python3
RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain nightly -y
ENV PATH="/root/.cargo/bin:${PATH}"

# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --yes build-essential pkg-config libssl-dev clang

# uncomment following two lines to be able to build libtensorflowlite_c.so with tflitec instead of library_builder
# RUN apt-get update && apt-get install --yes python3-full python3-pip git
# RUN python3 -m pip install numpy

# copy library, and set the ENV VAR
COPY --from=library_builder2 /tflite_build/libtensorflowlite_c.so /usr/lib/libtensorflowlite_c.so
ENV TFLITEC_PREBUILT_PATH_ARMV7_LINUX_ANDROIDEABI=/usr/lib/libtensorflowlite_c.so
ENV TFLITEC_PREBUILT_PATH=/usr/lib/libtensorflowlite_c.so

# cache rust dependencies
RUN mkdir /server && echo "fn main() {}" > /server/dummy.rs
COPY server/Cargo.toml /server/Cargo.toml
RUN sed -i 's#src/main.rs#dummy.rs#' /server/Cargo.toml
RUN cd /server && cargo build --release
RUN sed -i 's#dummy.rs#src/main.rs#' /server/Cargo.toml

# copy application and build
COPY server/src /server/src
RUN cd /server && cargo build --release

# step 3
# start FROM smallest Docker image that includes cc
FROM gcr.io/distroless/cc-debian12 as base  
COPY --from=library_builder2 /tflite_build/libtensorflowlite_c.so /usr/lib/libtensorflowlite_c.so
COPY --from=busybox /bin/sh /bin/sh
COPY --from=ubuntu /usr/bin/date /bin/date
COPY --from=ubuntu /usr/bin/tail /bin/tail
COPY model.tflite /model.tflite
COPY --from=application_builder /server/target/release/server /server

# step 4
FROM base
ENTRYPOINT ROCKET_ADDRESS=0.0.0.0 ROCKET_PORT=$PORT START_TIME=$(date +%s%N) /server


