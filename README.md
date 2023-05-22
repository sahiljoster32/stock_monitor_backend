# Getting Started with stock monitor backend.

## Steps to install backend service on you pc.

1. run `git clone https://github.com/sahiljoster32/stock_monitor_backend.git` into your console to clone the project.
2. go to inside cloned directory `cd stock_monitor_backend`.
3. run `pip install -r requirements.txt` to install all requirements.
4. run `python manage.py makemigrations` to make migrations for model, like `WatchList` model.
5. run `python manage.py migrate` to migrate all migrations to db schema.
6. run `python manage.py runserver` to start the serve, so that you can access the APIs.

## Model definition to store watchList.

![Model diagram](./model.png)

## [Demo link for working backend.](https://drive.google.com/file/d/1q0iEllNef7DDe66Knsf7ebhPFLyj-X1N/view?usp=sharing)

Thanks!
