# Python-ORM-2024

# Helpers

- [Populate Django DB Script](https://github.com/DiyanKalaydzhiev23/PopulateDjangoModel)

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

0. ORM - Предимства и недостатъци
   - Pros:
     -  Не ни се налага писането на low level SQL
     -  По-лесна поддръжка
     -  Добър при CRUD операции
   - Cons:
     - Не много оптимизиран за по-сложни заявки
     - Възможно е да влага излишна сложност в някои от заявките

2. Django models
   - Всеки модел е отделна таблица
   - Всяка променлова използваща поле от `models` е колона в тази таблица

3. Създаване на модели
   - Наследяваме `models.Model`
    

4. Migrations
   - `makemigrations` - създава миграции
   - `migrate` - прилага миграциите
  
5. Други команди
   - `dbshell` - отваря конзола, в коятоо можем да пишем SQL
   - `CTRL + ALT + R` - отваря manage.py console

---
