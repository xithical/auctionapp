FROM ubuntu:22.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt update \
    && apt -y --no-install-recommends install\
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        tzdata \
    && apt autoremove \
    && apt clean

COPY ./ ./

RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]