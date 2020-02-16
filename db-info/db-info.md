# DB Info

## DB Hostnames
We have 2 MySQL servers running: Dev and prod.

|   Type    | Hostname                                          |
|-----------|---------------------------------------------------|
|Developer  |`dev-db.cwybmrilj7cz.us-east-1.rds.amazonaws.com`  |
|Production |`prod-db.cgsyhdidac9y.us-east-1.rds.amazonaws.com` |

## DB Schema
The tables and columns for both databases (dev and prod) are in the files
`db-init-dev.sql` and `db-init-prod.sql` respectively. They're identical
at the moment. Both are under the database name `db`.

## Authentication
Both dev and prod databases use the same authentication user and password,
just for simplicity.

## How to Connect
You can connect using either the MySQL CLI application or the MySQL Workbench.
If using the CLI, use the following command:

`mysql -u 'admin' -p -h "hostname here"`

and enter the password.

If using the MySQL Workbench, enter in the username and hostname. Keep the
port default, and set SSL to `off`. Then click on the entry in the main
menu and enter the password to connect.