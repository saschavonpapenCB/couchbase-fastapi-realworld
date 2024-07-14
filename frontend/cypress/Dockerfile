FROM cypress/included:10.3.0

WORKDIR /e2e

COPY ../ /e2e

ENV CYPRESS_BASE_URL=http://frontend

CMD ["cypress", "run"]
