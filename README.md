# ![RealWorld Example App](logo.png)

> ### [FastAPI](https://github.com/tiangolo/fastapi) + Couchbase codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with [FastAPI](https://github.com/tiangolo/fastapi) + Couchbase including CRUD operations, authentication, routing, pagination, and more.


For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

> COMING SOON

## Prerequisites

To run this prebuilt project, you will need:

- [Couchbase Capella](https://www.couchbase.com/products/capella/) cluster with a bucket and scope loaded.
- [Python](https://www.python.org/downloads/) 3.9 or higher installed
  - Ensure that the Python version is [compatible](https://docs.couchbase.com/python-sdk/current/project-docs/compatibility.html#python-version-compat) with the Couchbase SDK.
- Using the Capella UI, create the following collections in the loaded scope, and using the Query data tool, create primary indicies for both:
  - `article`
  - `client` (`client` because `user` is a reserved Couchbase keyword)
```
CREATE PRIMARY INDEX ON `default`:`<bucket_name>`.`<scope_name>`.`<collection_name>`;
```

# Setting Up the Application

### Cloning Repo

```shell
git clone https://github.com/couchbase-examples/python-quickstart-fastapi.git
```

### Install Dependencies

The dependencies for the application are specified in the `requirements.txt` file in the root folder. Dependencies can be installed through `pip` the default package manager for Python.
```
python -m pip install -r requirements.txt
```
> Note: If your Python is not symbolically linked to python3, you need to run all commands using `python3` instead of `python`.

### Setup Database Configuration

To know more about connecting to your Capella cluster, please follow the [instructions](https://docs.couchbase.com/cloud/get-started/connect.html).

Specifically, you need to do the following:

- Create the [database credentials](https://docs.couchbase.com/cloud/clusters/manage-database-users.html) to access the travel-sample bucket (Read and Write) used in the application.
- [Allow access](https://docs.couchbase.com/cloud/clusters/allow-ip-address.html) to the Cluster from the IP on which the application is running.

All configuration for communication with the database is read from the environment variables. We have provided a convenience feature to read the environment variables from a local file, `.env` in the source folder.

Add the values for the Couchbase connection to the `.env` file.

> Note: Files starting with `.` could be hidden in the file manager in your Unix based systems including GNU/Linux and Mac OS.

```sh
DB_CONN_STR=<connection_string>
DB_USERNAME=<user_with_read_write_permission_to_travel-sample_bucket>
DB_PASSWORD=<password_for_user>
DB_BUCKET_NAME=<bucket_name>
DB_SCOPE_NAME=<scope_name>
```

> Note: The connection string expects the `couchbases://` or `couchbase://` part.

## Running The API

### Directly on Machine

At this point, we have installed the dependencies, setup the cluster and configured the api with the credentials. The api is now ready and you can run it.

```
./scripts/start-api.sh
```

### Using Docker

- Build the Docker image

```sh
docker build -t couchbase-fastapi-realworld . 
```

- Run the Docker image

```sh
docker run -it --env-file api/.env -p 8000:8000 couchbase-fastapi-realworld
```

> Note: The `.env` file has the connection information to connect to your Capella cluster. These will be part of the environment variables in the Docker container.


## Running Tests

To run RealWorld API tests, use the following command:

```
./scripts/realworld-test.sh
```

To run tests, use the following command:

```
./scripts/pytest-test.sh
```
