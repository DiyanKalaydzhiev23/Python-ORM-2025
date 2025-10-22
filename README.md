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

- [Migrations and Django Admin](https://forms.gle/7G2KzMujkCzHDgPb8)

---

- [Working with Queries](https://forms.gle/kieTF55zwmK2eAaM7)

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


### Migrations and Admin

1. Django Migrations Advanced
   - Миграциите ни помагат надграждаме промени в нашите модели
   - Както и да можем да пазим предишни стейтове на нашата база
   - Команди:
     - makemigrations
     - migrate
     - Връщане до определена миграция - migrate main_app 0001
     - Връщане на всички миграции - migrate main_app zero
     - showmigrations - показва всички апове и миграциите, които имат
     - showmigrations app_name - показва миграциите за един app
     - showmigrations --list - showmigrations -l 
     - squashmigrations app_name migration_to_which_you_want_to_sqash - събира миграциите до определена миграция в една миграция
     - sqlmigrate app_name migration_name - дава ни SQL-а на текущата миграция - използваме го, за да проверим дали миграцията е валидна
     - makemigrations --empty main_app - прави празна миграция в зададен от нас app

2. Custom/Data migrations
   - Когато например добавим ново поле, искаме да го попълним с данни на база на вече съществуващи полета, използваме data migrations
   - RunPython
     - викайки функция през него получаваме достъп до всички апове и техните модели (първи параметър), Scheme Editor (втори параметър)
     - добра практика е да подаваме фунцкия и reverse функция, за да можем да връщаме безпроблемно миграции
   - Scheme Editor - клас, който превръща нашия пайтън код в SQL, ползваме го когато правим create, alter и delete на таблица
     - използвайки RunPython в 95% от случаите няма да ни се наложи да ползавме Scheme Editor, освен, ако не правим някаква временна таблица
       индекси или промяна на схемата на таблицата
   - Стъпки:
     
      2.1. Създаваме празен файл за миграция: makemigrations --empty main_app - прави празна миграция в зададен от нас app
      
      2.2. Дефиниране на операции - Използваме RunPython за да изпълним data migrations
      
      2.3. Прилагане на промените - migrate

Пример с временна таблица:

Да приемем, че имате модел с име „Person“ във вашето Django приложение и искате да създадете временна таблица, за да съхранявате някои изчислени данни въз основа на съществуващите данни в таблицата „Person“. 
В този случай можете да използвате мигриране на данни, за да извършите тази операция:

1. **Create the Data Migration:**

Run the following command to create a data migration:

```bash
python manage.py makemigrations your_app_name --empty
```

This will create an empty data migration file.

2. **Edit the Data Migration:**

Open the generated data migration file and modify it to use `RunPython` with a custom Python function that utilizes the `SchemaEditor` to create a temporary table. Here's an example:

```python
from django.db import migrations, models

def create_temporary_table(apps, schema_editor):
    # Get the model class
    Person = apps.get_model('your_app_name', 'Person')

    # Access the SchemaEditor to create a temporary table
    schema_editor.execute(
        "CREATE TEMPORARY TABLE temp_person_data AS SELECT id, first_name, last_name FROM your_app_name_person"
    )

    ...

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', 'previous_migration'),
    ]

    operations = [
        migrations.RunPython(create_temporary_table),
    ]
```

3. Django admin
   - createsuperuser
   - Register model, example:
   
   ```python
      @admin.register(OurModelName)
      class OurModelNameAdmin(admin.ModelAdmin):
   	pass
   ```
4. Admin site customizations
  - __str__ метод в модела, за да го визуализираме в админ панела по-достъпно

  - list_display - Показваме различни полета още в админа
    Пример: 
    ```python
    class EmployeeAdmin(admin.ModelAdmin):
    	list_display = ['job_title', 'first_name', 'email_address']
    ```

  - List filter - добавя страничен панел с готови филтри
    Пример:

      ```python
       class EmployeeAdmin(admin.ModelAdmin):
       	list_filter = ['job_level']
      ```

  - Searched fields - казваме, в кои полета разрешаваме да се търси, по дефолт са всички
    Пример:
    
    ```python
    class EmployeeAdmin(admin.ModelAdmin):
        search_fields = ['email_address']
    ```
  
  - Layout changes - избираме, кои полета как и дали да се появяват при добавяне или промяна на запис
    Пример:
    
    ```python
    class EmployeeAdmin(admin.ModelAdmin):
        fields = [('first_name', 'last_name'), 'email_address']
    ```

  - list_per_page
   
  - fieldsets - променяме визуално показването на полетата
    Пример:
    ```python
      fieldsets = (
           ('Personal info',
            {'fields': (...)}),
           ('Advanced options',
            {'classes': ('collapse',),
           'fields': (...),}),
      )
    ```

---

### Data Operations in Django with queries


1. CRUD overview
   - CRUD - Create, Read, Update, Delete
   - Използваме го при: 
     - Web Development
     - Database Management
   - Дава ни един консистентен начин, за това ние да създаваме фунцкионалност за CRUD
   - Можем да го правим през ORM-a на Джанго

2. Мениджър в Django:
    - Атрибут на ниво клас на модел за взаимодействия с база данни.
    - Отговорен за CRUD
    - Custom Manager: Подклас models.Manager.
       - Защо персонализирани мениджъри:
         - Капсулиране на общи или сложни заявки.
         - Подобрена четимост на кода.
         - Избягвайме повторенията и подобряваме повторната употреба.
         - Промяна наборите от заявки според нуждите.

3. Django Queryset
   - QuerySet - клас в пайтън, които изпозваме, за да пазим данните от дадена заявка
   - Данните не се взимат, докато не бъдат потърсени от нас
   - cars = Cars.objects.all() # <QuerySet []>
   - print(cars)  # <QuerySet [Car object(1)]>

   - QuerySet Features: 
     - Lazy Evaluation - примера с колите, заявката не се вика, докато данните не потрябват
     - Retrieving objects - можем да вземаме всички обекти или по даден критерии
     - Chaining filters - MyModel.objects.filter(category='electronics').filter(price__lt=1000)
     - query related objects - позволява ни да търсим в таблици, с които имаме релации, през модела: # Query related objects using double underscores
related_objects = Order.objects.filter(customer__age__gte=18)
     - Ordering - ordered_objects = Product.objects.order_by('-price')
     - Pagination 
      ```python
       from django.core.paginator import Paginator

        # Paginate queryset with 10 objects per page
        paginator = Paginator(queryset, per_page=10)
        page_number = 2
        print([x for x in paginator.get_page(2)])
      ```

4. Django Simple Queries
   - Object Manager - default Objects
   - Methods:
     - `all()`
     - `first()`
     - `get(**kwargs)`
     - `create(**kwargs)`
     - `filter(**kwargs)`
     - `order_by(*fields)`
     - `delete()`

5. Django Shell and SQL Logging
   - Django Shell
     - Дава ни достъп до целия проект
     - python manage.py shell
   - SQL logging
     -  Enable SQL logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Other levels CRITICAL, ERROR, WARNING, INFO, DEBUG
    },
    'loggers': {
        'django.db.backends': {  # responsible for the sql logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---
