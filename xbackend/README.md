# An X-like Demo App following Code With Stein on YouTube

- [Build a Full-Stack Social Network with Django and Vue 3](https://www.youtube.com/watch?v=xOxN_7coIDw&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO)

## xbackend - Django + DRF + JWT

```shell
cd xbackend
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

- Altenatively, setting the local PyPi mirror permanently makes things easier

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt

pip config unset global.index-url (Unset)
```

## Migrate the DB (Order matters!)

```shell
python manage.py makemigrations
python manage.py migrate
```

## Remove existing migrations and DB

```shell
python del_migrations.py
```

## Populate or clear the project result table

```shell
python manage.py seed_result --project_results=10
python manage.py seed_result --clear
```

## Start the backend

```shell
python manage.py runserver 0.0.0.0:8001
```

## Poupulate the DB with fake data

### The default args with 50 formations, 5 workspaces, & 20 projects

```shell
python manage.py seed_db
```

### Use your custom counts

```shell
python manage.py seed_db  --formations=500 --workspaces=10 --projects=50
```

### Clear the populated formations, workspaces, & projects

```shell
python manage.py seed_db --clear
```

### Run the tests

```shell
pytest        (full tests)
pytest -v     (verbose)
pytest -vv    (very verbose)
pytest -rP    (report the print output)
pytest -x     (stop at the fist failure)
pytest tests  (against a folder/package)
pytest tests/test_account.py  (against a module)
pytest tests/test_account.py::test_model_update  (against a specific test)
```

### Enable the pytest watching mode

```shell
pip install pytest-watcher
ptw . (or, ptw /home/repos/project)
```

### Show the test coverage

```shell
pytest --cov
```
