FROM python:3.13-alpine

ARG user=docs
ARG group=pyflowops
ARG CACHE_BREAKER=1

# Install dependencies, tools and install the gh CLI
RUN apk add --no-cache \
    bash \
    github-cli \
    curl

#RUN curl -sS https://webi.sh/gh | sh

# In order for the gh CLI to work in the environment, we need to set the PATH
# This way, we can invoke it from the command line from anywhere
# The gh CLI is installed in /root/.local/bin by default
ENV PATH="/root/.local/bin:${PATH}"
ENV PORT=8100
ENV HOST="0.0.0.0"

RUN addgroup ${group}
RUN adduser -D ${user} -G ${group}

WORKDIR /app
COPY . .
RUN chown -R ${user}:${group} /app \
    && chmod 755 /app/docker/docs/entrypoint.sh

# Set the user to the one we created
USER ${user}

RUN python -m pip install --upgrade pip && python -m pip install -r /app/docs/production.txt
EXPOSE ${PORT}

ENTRYPOINT ["/app/docker/docs/entrypoint.sh"]
