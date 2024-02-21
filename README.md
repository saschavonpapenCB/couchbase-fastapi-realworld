# ![RealWorld Example App](logo.png)

> ### [FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### (https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with **[FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the [FastAPI](https://github.com/tiangolo/fastapi) + [Couchbase] community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

> Describe the general architecture of your app here

# Prerequisites

> Couchbase Capella cluster with bucket and scope loaded.
Details to be put in the .env file.

> Create an 'article' and a 'client' collection in the loaded scope ('client' because 'user' is a reserved Couchbase keyword).

> Create collection primary indicies.
```
CREATE PRIMARY INDEX ON `default`:`BUCKET_NAME`.`SCOPE_NAME`.`COLLECTION_NAME`;
```

# Getting started

> Install dependencies.
Run this command:
```
./scripts/install-deps.sh
```

> Run API.
Run this command:
```
./scripts/start-api.sh
```

# Testing

> Run Pytest.
Run this command:
```
./scripts/pytest-test.sh
```

> Run RealWorld API test:
Run this command:
```
./scripts/realworld-test.sh
```
