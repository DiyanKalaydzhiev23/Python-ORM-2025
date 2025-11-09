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

- [Data Operations with Django Queries](https://forms.gle/Pzay1RHaUuQCb1X68)

---

- [Working with Queries](https://forms.gle/kieTF55zwmK2eAaM7)

---

- [Django Relations](https://forms.gle/6uvQdwzqfxt87kD36)

---

- [Models Inheritance](https://forms.gle/jgC7Mk67gmaaNGvd7)

---

- [Advanced Models Techniques](https://forms.gle/gcqt9VcQvbmuaYbCA)

---

- [Advanced Django Queries](https://forms.gle/Q1BJDMCQ8NfSBbWg8)

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


### Working with queries

Working with Queries


1. Useful Methods
   - filter() - връща subset от обекти; приема kwargs; връща queryset;
   - exclude() - връща subset от обекти; приема kwargs; връща queryset;
   - order_by() - връща сортираните обекти; - за desc;
   - count() - като len, но по-бързо; count връща само бройката без да му трябвата реалните обекти;
   - get() - взима един обект по даден критерии;


2. Chaning methods
   - всеки метод работи с върнатия от предишния резултат


3. Lookup keys
   - Използват се във filter, exclude, get;
   - __exact __iexact - матчва точно;
   - __contains __icontains - проверява дали съдържа;
   - __startswith __endswith
   - __gt __gte
   - __lt __lte
   - __range=(2, 5) - both inclusive

4. Bulk methods
   - използват се за да извършим операции върху много обекти едновременно
   - bulk_create - създава множество обекти навъеднъж;
   - filter().update()
   - filter().delete()

---

###  Django Relations

Django Models Relations


1. Database Normalization
   - Efficient Database Organization
     - Data normalization - разбива големи таблици на по-малки такива, правейки данните по-организирани
     - Пример: Все едно имаме онлайн магазин и вместо да пазим име, адрес и поръчка в една таблица, можем да разбием на 3 таблици и така да не повтаряме записи
   
    - Guidelines and Rules
    - First Normal Form
		- First Normal Form (1NF): елеминираме повтарящите се записи, всяка таблица пази уникални стойности
	    - Всяка колона съдържа атомарни (неделими) стойности, тоест не пазим списъци.
		- Няма повтарящи се групи или масиви от стойности в една клетка.
	 	- Всеки ред е уникален (има идентификатор или PK).

	- Second Normal Form (2NF): извършваме първото като го правим зависимо на PK
	  	- Пример: Онлайн магазин с данни и покупки Customers и Orders са свързани с PK, вместо всичко да е в една таблица
        - Имаме таблица с (OrderID, ProductID, ProductName, Quantity)
		- ProductName зависи само от ProductID, не от целия съставен ключ (OrderID, ProductID) - нарушава 2NF
		- Решение: разделяме на таблици Orders и Products.

	- Third Normal Form (3NF):
	  - Премахване на преходни зависимости (транзитивни зависимости), при които една неключова колона зависи от друга неключова колона, а не директно от първичния ключ.
	  - Ако таблица съдържа данни като ID на служител, име на служител, град и пощенски код, но пощенския код зависи от града, а не директно от служителя, тогава съществува транзитивна зависимост.
	  - За да изпълним 3NF, разделяме информацията в три таблици – служители, градове и адреси.
	  - Връзките между тях не е задължително да са по първичен ключ (PK), а могат да бъдат по city_id, така че служителят да не бъде зависим от конкретния адрес, а само от града, в който работи.
        
	- Boyce-Codd Normal Form (BCNF):
      - По-строга версия на 3NF
      - Тук правим да се навързват по PK
	  - Таблицата е в BCNF, ако при всяка зависимост X → Y, X е суперключ (уникално определя реда).  
	  - Тоест — няма колона, която да определя друга, без да е уникален идентификатор.
			
			**Пример:**  
			| Professor | Subject | Room |  
			|------------|----------|------|  
			| Иванов     | БД       | 101  |  
			| Иванов     | Програмиране | 101 |  
			
			Тук `Professor → Room`, но `Professor` не е суперключ → нарушава BCNF.  
			Решение: разделяме на `ProfessorsRooms` и `ProfessorsSubjects`.


	- Fourth Normal Form (4NF):
	  - Една таблица е в 4NF, ако е в Трета Нормална Форма (3NF) и няма многозначни зависимости (multivalued dependencies - MVDs).
	  - Многозначна зависимост възниква, когато един ключ (например "Курс") е свързан с множество стойности на два или повече независими набора от данни.
     	  - Например, ако имаме таблица с колони, "Курс", "Лектор", "Книга", можем да я разделим на две таблици. Курс - Лектор, Курс - Книга.
	    	```
	        Курс	Книга	Преподавател
			X	A	Иванов
			X	B	Иванов
			Y	A	Петров
			Y	C	Петров
	     	```
        - Трябва да се раздели на 2 таблици
        - Курс - Книга
          ```
			Курс	Книга
			X	A
			X	B
			Y	A
			Y	C
          ```
        - Курс - Преподавател
		  ```
			Курс	Преподавател
			X	Иванов
			Y	Петров
	 	  ```
	- Fifth Normal Form (5NF) - Project-Join Normal Form or PJ/NF:
	  - Кратко казано да не ни се налага да минаваме през таблици с данни, които не ни трябват, за да достигнем до таблица с данни, която ни трябва

   - Database Schema Design
      - Създаването на различни ключове и връзки между таблиците

   - Minimizing Data Redundancy
     - Чрез разбиването на таблици бихме имали отново намалено повтаряне на информация
     - Имаме книга и копия, копията са в отделна таблица, и са линкнати към оригинала
   
   - Ensuring Data Integrity & Eliminating Data Anomalies
     - Това ни помага да update-ваме и изтриваме данните навсякъде еднакво
     - отново благодарение на някакви constraints можем да променим една стойност в една таблица и тя да се отрази във всички

   - Efficiency and Maintainability
     - Благодарение на по-малките таблици, ги query–ваме и update-ваме по-бързо

1. Релации в Django Модели
   - Получават се използвайки ForeignKey полета
   - related_name - можем да направим обартна връзка
     - По дефолт тя е името + _set
  
   - Пример:
   ```py
   class Author(models.Model):
       name = models.CharField(max_length=100)
   
   class Post(models.Model):
       title = models.CharField(max_length=200)
       content = models.TextField()
       author = models.ForeignKey(Author, on_delete=models.CASCADE)
   ```

- Access all posts written by an author
```py
author = Author.objects.get(id=1)
author_posts = author.post_set.all()
```

3. Types of relationships
   - Many-To-One (One-To-Many)
   - Many-To-Many 
     - Няма значение, в кой модел се слага
     - Django автоматично създава join таблица или още наричана junction
     - Но, ако искаме и ние можем да си създадем: 
      ```py
      class Author(models.Model):
          name = models.CharField(max_length=100)
      
      class Book(models.Model):
          title = models.CharField(max_length=200)
          authors = models.ManyToManyField(Author, through='AuthorBook')
      
      class AuthorBook(models.Model):
          author = models.ForeignKey(Author, on_delete=models.CASCADE)
          book = models.ForeignKey(Book, on_delete=models.CASCADE)
          publication_date = models.DateField()
      ```

   - OneToOne, предимно се слага на PK
   - Self-referential Foreign Key
      - Пример имаме работници и те могат да са мениджъри на други работници
        
   ```py
   class Employee(models.Model):
       name = models.CharField(max_length=100)
       supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
   ```

    - Lazy Relationships - обекта от релацията се взима, чрез заявка, чак когато бъде повикан

---


### Models Inheritance and Customization

1. Типове наследяване
   - Multi-table
     - Разширяваме модел с полетата от друг модел, като не копираме самите полета, а използваме създадения от django pointer, който прави One-To-One Relationship
     - Пример: 

	```py
	class Person(models.Model):
	    name = models.CharField(max_length=100)
	    date_of_birth = models.DateField()
	    
	    def is_student(self):
	        """Check if this person is also a student."""
	        return hasattr(self, 'student')
	
	class Student(Person):
	    student_id = models.CharField(max_length=15)
	    major = models.CharField(max_length=50)
	```	


   - Abstract Base Classes
     - При това наследяване не се създават две нови таблици, а само една и тя е на наследяващия клас(Child), като абстрактния клас(Parent) е само шаблон
     - Постигаме го чрез промяна на Meta класа:
       ```py
       class AbstractBaseModel(models.Model):
           common_field1 = models.CharField(max_length=100)
           common_field2 = models.DateField()
    
           def common_method(self):
               return "This is a common method"
    
           class Meta:
               abstract = True
       ```

   - Proxy Models
     - Използваме ги, за да добавим функционалност към модел, който не можем да достъпим
     - Можем да добавяме методи, но не и нови полета
     - Пример:

	```py
	class Article(models.Model):
	    title = models.CharField(max_length=200)
	    content = models.TextField()
	    published_date = models.DateField()
	
	class RecentArticle(Article):
	    class Meta:
	        proxy = True
	
	    def is_new(self):
	        return self.published_date >= date.today() - timedelta(days=7)
	    
	    @classmethod
	    def get_recent_articles(cls):
	        return cls.objects.filter(published_date__gte=date.today() - timedelta(days=7))
	```

2. Основни Built-In Методи
   - `save()` - използва се за запазване на записи
	```py
	    def save(self, *args, **kwargs):
	        # Check the price and set the is_discounted field
	        if self.price < 5:
	            self.is_discounted = True
	        else:
	            self.is_discounted = False
	
	        # Call the "real" save() method
	        super().save(*args, **kwargs)
	```
   - `clean()` - използва се, когато искаме да валидираме логически няколко полета, например имаме тениска в 3 цвята, но ако е избран XXL цветовете са само 2.
 

3. Custom Model Properties
   - Както и в ООП, можем чрез @property декоратора да правим нови атрибути, които в случая не се запазват в базата
   - Използваме ги за динамични изчисления на стойностти

4. Custom Model Fields
   - Ползваме ги когато, Django няма field, които ни върши работа
   - Имаме методи като:
     - from_db_value - извиква се, когато искаме да взмем стойността от базата в пайтън
     - to_python - извиква се когато правим десериализация или clean
     - get_prep_value - обратното на from_db_value, от Python към базата, предимно ползваме за сериализации
     - pre_save - използва се за last minute changes, точно преди да запазим резултата в базата

	```py
	class RGBColorField(models.TextField):
	    # Convert the database format "R,G,B" to a Python tuple (R, G, B)
	    def from_db_value(self, value, expression, connection):
	        if value is None:
	            return value
	        return self.to_python(value)
	
	    # Convert any Python value to our desired format (tuple)
	    def to_python(self, value):
	        if isinstance(value, tuple) and len(value) == 3:
	            return value
	        if isinstance(value, str):
	            return tuple(map(int, value.split(',')))
	        raise ValidationError("Invalid RGB color format.")
	
	    # Prepare the tuple format for database insertion
	    def get_prep_value(self, value):
	        # Convert tuple (R, G, B) to "R,G,B" for database storage
	        return ','.join(map(str, value))
	```

---

### Advanced Django Models Techniques
 

1. Validation in Models
   - Built-in Validators
     - MaxValueValidator, MinValueValidator - приема два аргумета (limit, message)
     - MaxLengthValidator, MinLengthValidator - приема два аргумета (limit, message)
     - RegexValidator - приема два аргумета (regex, message)
	```py
	class SampleModel(models.Model):
	    name = models.CharField(
	        max_length=50,
	        validators=[MinLengthValidator(5)]  # Name should have a minimum length of 5 characters
	    )
	
	    age = models.IntegerField(
	        validators=[MaxValueValidator(120)]  # Assuming age shouldn't exceed 120 years
	    )
	
	    phone = models.CharField(
	        max_length=15,
	        validators=[
		    RegexValidator(
		        regex=r'^\+?1?\d{9,15}$',
	                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
		)]  # A simple regex for validating phone numbers
	    )
	```
 - Custom Validators - функции, които често пишем в отделен файл. При грешка raise-ваме ValidationError


2. Meta Options and Meta Inheritance
   - В мета класа можем да променяме:
     - Името на таблицата
     - Подреждането на данните
     - Можем да задаваме constraints
     - Можем да задаваме типа на класа(proxy, abstract)
	```py
	class SampleModel(models.Model):
	    name = models.CharField(max_length=50)
	    age = models.IntegerField()
	    email = models.EmailField()
	
	    class Meta:
	        # Database table name
	        db_table = 'custom_sample_model_table'
	
	        # Default ordering (ascending by name)
	        ordering = ['name'] - Случва се на SELECT, не на INSERT
	
	        # Unique constraint (unique combination of name and email)
	        unique_together = ['name', 'email']
	```
    - Meта наследяване:
      - Ако наследим абстрактен клас и не презапишем мета класа, то наслеяваме мета класа на абстрактния клас
	```py
	class BaseModel(models.Model):
	    name = models.CharField(max_length=100)
	    
	    class Meta:
	        abstract = True
	        ordering = ['name']
	
	class ChildModel(BaseModel):
	    description = models.TextField()
	    # ChildModel inherits the Meta options
	```

3. Indexing
   - Индексирането ни помага, подреждайки елементите в определен ред или създавайки друга структура, чрез, която да търсим по-бързо.
   - Бързо взимаме записи, но ги запазваме по-бавно
   - В Django можем да сложим индекс на поле, като добавим key-word аргумента db_index=True
   - Можем да направим и индекс, чрез мета класа, като можем да правим и композитен индекс
	```py
	class Meta:
	indexes=[
	models.Index(fields=["title", "author"]),  # прави търсенето по два критерия, по-бързо
	models.Index(fields=["publication_date"])
	]
	```


4. Django Model Mixins
   - Както знаем, миксините са класове, които използваме, за да отделим обща функционалност

	```py
	class TimestampMixin(models.Model):
	    created_at = models.DateTimeField(auto_now_add=True)
	    updated_at = models.DateTimeField(auto_now=True)
		class Meta:
	    	    abstract = True
	```

---


### Advanced Django Queries

1. Custom managers
   - Използваме ги, за да изнсем бизнез логиката, за често използвани заявки на едно място
   - Правим го наследявайки мениджъра по подразбиране.
	
	```py
	    class BookManager(models.Manager):
	        def average_rating(self):
	            # Calculate the average rating of all books
	            return self.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
	
	        def highest_rated_book(self):
	            # Get the highest-rated book
	            return self.order_by('-rating').first()
	```

2. Annotations and Aggregations
   - Анотации - използваме ги, за да добавяме нови полета във върнатия резултат, често на база някакви изчисления. Връща QuerySet.
   - Пример:
	
	```py
	# Annotating the queryset to get the count of books for each author
	authors_with_book_count = Book.objects.values('author').annotate(book_count=Count('id'))
	```
   - Агрегации - връщат едно поле(една стойност), често резултат от агрегиращи функции. Връща dict
	
	```py
	# Annotating the queryset to get the average rating of all books
	average_rating = Book.objects.aggregate(avg_rating=Avg('rating'))
	```

3. `select_related` & `prefetch_related`

Общо
Използват се за оптимизация на заявки и избягване на N+1 проблема.

---

 `select_related`
- Работи при **OneToOne** и **ForeignKey (Many-To-One)**.
- Прави **JOIN** и взима свързаните обекти в една заявка.
- Използва се при релации, които връщат само един обект.
- Поддържа няколко и вложени връзки (`'author__country'`).

```py
books = Book.objects.select_related('author', 'publisher')
# SELECT ... FROM book
# LEFT JOIN author ON ...
# LEFT JOIN publisher ON ...
```

---

 `prefetch_related`
- Работи при **ManyToMany** и **reverse ForeignKey (One-To-Many)**.
- Прави отделни заявки и join-ва в Python.
- Използва се при релации, които връщат много обекти.
- Може да се комбинира с `Prefetch` за филтриране или `to_attr`.

```py
authors = Author.objects.prefetch_related('book_set')
# 1) SELECT * FROM author;
# 2) SELECT * FROM book
#    INNER JOIN book_authors ON ...
```

---

Комбиниране
```py
Book.objects.select_related('author__country', 'publisher') \
            .prefetch_related('genres', 'reviews')
```

---

4. Q and F

  - Използваме Q object, за да правим заявки изискващи по-сложни условия
  - Пример:

	```py
	q = Q(title__icontains='Django') & (Q(pub_year__gt=2010) | Q(author='John Doe'))
	
	books = Book.objects.filter(q)
	
	``` 

  - Използваме F object, за да достъпваме, стойностите през, които итерираме на ниво SQL

	```py
	from django.db.models import F
	
	Book.objects.update(rating=F('rating') + 1)
	```

---

