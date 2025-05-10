FROM python:3.12.6-alpine

ARG user=docs
ARG group=docs
RUN addgroup ${group}
RUN adduser -D ${user} -G ${group}

USER ${user}
WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip && python -m pip install -r docs/production.txt
EXPOSE 8100

CMD ["python", "-m", "mkdocs", "serve", "--dev-addr=0.0.0.0:8100"]
