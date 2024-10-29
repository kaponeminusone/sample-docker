FROM python:3.9

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN python -m venv .venv
RUN /bin/bash -c "source v.env/bin/activate"

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8080


