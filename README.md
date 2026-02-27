# An X-like Demo App following Code With Stein on YouTube

## xfrontend - Vue.js 3 + TypeScript + Tailwind CSS

```shell
cd xfrontend
npm install --registry=https://registry.npmmirror.com
```

## xbackend - Django + DRF + JWT

```shell
cd xbackend
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

Altenatively, setting the local PyPi mirror permanently makes things easier

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

## Backend Tests

### Run the tests

```shell
pytest        (full tests)
pytest -v     (verbose)
pytest -vv    (very verbose)
pytest -rP    (report the print output)
pytest -x     (stop at the fist failure)
pytest tests  (against a folder/package)
pytest tests/apps/basic_data/model_test.py  (against a module)
pytest tests/apps/basic_data/model_test.py::test_model_update  (against a specific test)
```

### Show the test coverage

```shell
pytest --cov
```

## Frontend Tests

### Install the dependencies

```shell
npm install -D vitest @vue/test-utils happy-dom @testing-library/vue @pinia/testing
```
Note:
 - vitest is for unit-testing plain JS/TS;
 - @vue/test-utils is for unit-testing the components;
 - @testing-library/vue is for unit-testing composables;
 - Happy DOM is designed to work seamlessly with testing frameworks. It allows developers to simulate a DOM environment for running unit tests for front-end projects without relying on a browser.
