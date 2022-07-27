@echo off

@title start app

@echo --------------------
@echo устанавливаем pipenv
@echo --------------------

@python  -m pip install --upgrade pip
@pip install pipenv

@echo -------------------------------------
@echo поднимаем виртуальное окружение .venv
@echo -------------------------------------

@set /a PIPENV_VENV_IN_PROJECT=1
pipenv install

@echo -------------------------------------
@echo запускаем заполнение базы
@echo -------------------------------------

pipenv run alembic revision --autogenerate
pipenv run alembic upgrade head
@echo -------------------------------------
@echo запускаем проект
@echo -------------------------------------
rem start cmd /k pipenv run python script.py
pipenv run python main.py