<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/SilvaMoreno/scripts">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
    <h2 align="center">Dev scripts</h2>
  </a>

  <p align="center">
    Script for developers using linux
    <br />
    <a href="https://github.com/SilvaMoreno/scripts"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SilvaMoreno/scripts/issues">Report Bug</a>
    ·
    <a href="https://github.com/SilvaMoreno/scripts/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#docker">Docker</a>
      <ul>
        <li><a href="#postgres">Postgres</a></li>
        <li><a href="#mysql">Mysql</a></li>
      </ul>
    </li>
    <li>
      <a href="#multiple-ssh-keys-settings-for-different-account">Multiple SSH Keys settings for different account</a>
    </li>
  </ol>
</details>

<!-- GETTING STARTED -->

## Docker

### Postgres

Create network

```sh
$ docker network create --driver bridge postgres-network
```

- PosgresSQL
Replace **_POSTGRES_PASSWORD_** to your postgres password and **_POSTGRES_FOLDER_PATH_** to your postgres local folder

```sh
$ sudo docker run --name my-postgres --network=postgres-network -e "POSTGRES_PASSWORD=_POSTGRES_PASSWORD_" -p 5432:5432 -v _POSTGRES_FOLDER_PATH_:/var/lib/postgresql/data -d postgres
```

Iterative mode

```sh
$ docker exec -it my-postgres bash
```

- PG Admin
  Local url: localhost:8888
Default user is **pgadmin@pgadmin.com** and password **pgadmin**
```sh
$ sudo docker run --name my-pgadmin --network=postgres-network -p 8888:80 -e "PGADMIN_DEFAULT_EMAIL=pgadmin@pgadmin.com" -e "PGADMIN_DEFAULT_PASSWORD=pgadmin" -d dpage/pgadmin4
```

### MySql

```sh
$ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql
```

### Multiple SSH Keys settings for different account

create different ssh key (with custom name)

```sh
$ ssh-keygen
```

for example, keys created at:

```sh
~/.ssh/gitlab_key
```

get content of generated ssh key and add it to your git repository

```sh
$ cat ~/.ssh/gitlab_key.pub
```

Modify the ssh config

```sh
$ cd ~/.ssh/
$ touch config
```

Then added

```
Host [username].[github|gitlab].com
	HostName [github|gitlab].com
	PreferredAuthentications publickey
	IdentityFile ~/.ssh/gitlab_key
```
