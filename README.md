# ![RealWorld Example App](logo.png)

> ### [FastAPI](https://github.com/tiangolo/fastapi) + Couchbase codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with [FastAPI](https://github.com/tiangolo/fastapi) + Couchbase including CRUD operations, authentication, routing, pagination, and more.


For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

> TBC

# Prerequisites

> Create a Couchbase Capella cluster with bucket and scope loaded.
Cluster details to be put in the .env file.

> Create an 'article' and a 'client' collection in the loaded scope on the cluster ('client' because 'user' is a reserved Couchbase keyword).

> Create primary indicies for both collection.
```
CREATE PRIMARY INDEX ON `default`:`BUCKET_NAME`.`SCOPE_NAME`.`COLLECTION_NAME`;
```

# Getting started

> Install dependencies:
```
./scripts/install-deps.sh
```

> Run API:
```
./scripts/start-api.sh
```

# Testing

> Run Pytest:
```
./scripts/pytest-test.sh
```

> Run RealWorld API test:
```
./scripts/realworld-test.sh
```
