# Django ORM

# Helpers

- [File Zipper](https://github.com/DiyanKalaydzhiev23/FileZipper/tree/main)

- [Populate Django DB Script](https://github.com/DiyanKalaydzhiev23/PopulateDjangoModel)

### Zip on mac/linux
```shell
zip -r project.zip . -x "*.idea*" -x "*.venv*" -x "*__pycache__*"
```

### Zip on Windows
```shell
Get-ChildItem -Path . -Recurse -Force |
  Where-Object { $_.FullName -notmatch "\.idea|\.venv|__pycache__" } |
  Compress-Archive -DestinationPath .\project.zip

```

# Theory Tests

---

- [Django Models Basics](https://forms.gle/JwTbUtEkddw2Kc2R7)

---


# Plans

--- 

### Django Models

```
ORM - Object Relational Mapping
```

1. Django models
   - Всеки модел е отделна таблица
   - Всяка променлова използваща поле от `models` е колона в тази таблица
   - Моделите ни позволяват да не ни се налага писането на low level SQL

2. Създаване на модели
   - Наследяваме `models.Model`
    

3. Migrations
   - `makemigrations`
   - `migrate`
  
4. Други команди
   - `dbshell` - отваря конзола, в която можем да пишем SQL
   - `CTRL + ALT + R` - отваря manage.py console

---

