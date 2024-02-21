# ![RealWorld Example App](logo.png)

> ### [FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### (https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with **[FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the [FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

> Describe the general architecture of your app here

# Prerequisites

> Couchbase Capella cluster with bucket loaded.

# Getting started

> 






IMPLEMENT COUCHBASE PRIMARY INDEXES:
CREATE PRIMARY INDEX ON `default`:`travel-sample`.`inventory`.`COLLECTION_NAME`;



RUN API:
```
./scripts/start-api.sh
```

RUN REALWORLD TEST:
```
./scripts/realworld-test.sh
```

RUN PYTEST:
```
./scripts/pytest-test.sh
```