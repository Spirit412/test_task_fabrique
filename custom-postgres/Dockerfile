FROM postgres:12

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-12-first-last-agg \
      && rm -rf /var/lib/apt/lists/*

COPY create-extension.sh /docker-entrypoint-initdb.d/