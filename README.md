# questioner-api

Questioner crowd-source questions for a meetup and it helps the meetup organizer prioritize questions to be answered.

### Running the app using docker

- Install docker

  ```
  brew cask install docker

  ```

  OR  
  [Install by downloading dmg file](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

- Create django and database services

  ```
  make build
  ```

- Create database by running `make psql` then

  ```
  CREATE DATABASE quiz_db;
  ```

- Run migrations

  - Initial migrations

    ```
    make migrate

    ```

  - New model or update of existing models

    ```
    make migrations

    ```

- Run application

  ```
  make run-app
  ```

- Check services status

  ```
  make status

  ```

- Start all services

  ```
  make start
  ```

- Start services individually

  ```
  make start service=<service name>
  ```

- Stop all services

  ```
  make stop
  ```

- Stop services individually

  ```
  make stop service=<service name>
  ```

- Stop and remove all services

  ```
  make down
  ```

### Running locally without docker

- Ensure you have python 3, pipenv and postgress are installed
- Create virtual environment and installed required packages by running

  ```
  pipenv install
  ```

- Enter virtual environment by running

  ```
  pipenv shell
  ```

- Create database by running `psql` then

  ```
  CREATE DATABASE quiz_db;
  ```

- Run migrations

  - Initial migrations

    ```
    python manage.py migrate

    ```

  - New models or updates of existing models

    ```
    python manage.py makemigrations

    ```

- To run the application run
  ```
  python manage.py runserver
  ```
