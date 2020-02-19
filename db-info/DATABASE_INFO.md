# Database Info

## Database Hostnames

There are two MySQL servers running: Dev and prod.

|   Type    | Hostname                  |
|-----------|---------------------------|
|Developer  |`dev-db.findmythrone.com`  |
|Production |`prod-db.findmythrone.com` |

## Database Schema

The tables and columns for both databases (dev and prod) are in the files
`db-init-dev.sql` and `db-init-prod.sql` respectively. Both are under the database name `db`.

## Authentication

Both dev and prod databases use the same authentication user and password.

## How to Connect

You can connect using either the MySQL CLI application or an SQL client.

### MySQL CLI

1. Use the following command:

    ```shell
    mysql -u 'admin' -p -h "hostname here"
    ```

2. Enter the password for the database.

### SQL Client

Create a new database connection and use the following settings:

* username `admin`.
* Dev or Prod hostname.
* Default port.
* SSL `off`.
* Enter the password.
