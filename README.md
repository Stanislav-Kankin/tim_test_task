# 🛍️ Telegram Shop Bot + Django Admin Panel

Проект состоит из двух частей:
- **Telegram-бот** (на `aiogram 3`)
- **Админ-панель** (на `Django 4.2`)
- Общая база данных `PostgreSQL`

---

## 📁 Структура проекта

```
.
├── admin_panel
│   ├── admin_panel
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── media
│   ├── orders
│   ├── product_images
│   └── requirements.txt
├── bot
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── img
│   ├── media
│   ├── requirements.txt
│   └── src
├── docker-compose.yml
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   └── pyvenv.cfg
└── README.md
```

---

## ⚙️ Установка и запуск

### 1. Клонировать проект
```bash
git clone <URL>
cd tim_test_task
```


### 2. Настроить переменные .env
Создай файл .env в корне проекта:

```
BOT_TOKEN=your_token_bot
POSTGRES_DB=db_shop
POSTGRES_USER=stanislav
POSTGRES_PASSWORD=12345
POSTGRES_HOST=db
POSTGRES_PORT=5432
```


### 3. Запуск в Docker

```
docker-compose down --volumes --remove-orphans
docker image prune -a -f
docker-compose build --no-cache
docker-compose up
```

## Это:

Скачает образы

Соберёт и запустит бота и админку

Применит миграции

Создаст суперпользователя: admin / admin123

### 🧪 Доступы

```
| Компонент    | Адрес                                                        |
| ------------ | ------------------------------------------------------------ |
| Django Admin | http://localhost:8000/admin/ 
| Telegram-бот | Поиск по username в Telegram                                 |
```

### ⚡ Возможности
## 📱 Telegram-бот:
Категории и подкатегории с пагинацией

Просмотр товаров с фото и ценами

Добавление в корзину

Оформление заказа (будет добавлено оплата)

## 🛠️ Django Admin:
Управление товарами, категориями, подкатегориями

Пользователи и их корзины

Заказы

## 📢 Рассылки (с текстом и фото)

Можно отправить сразу кнопкой "Отправить сейчас"

## 📤 Загрузка фото
Все изображения хранятся в admin_panel/media/product_images/

Подключены в Docker и доступны боту

Загрузить фото можно в админке при создании товара

### 🐞 Типичные ошибки и решения
## Ошибка relation does not exist
→ Выполни миграции вручную:

```
docker-compose exec admin python manage.py makemigrations
docker-compose exec admin python manage.py migrate
```

## Изменил поля в models.py, но не видно в БД
→ Удали старые миграции и пересоздай:

```
find admin_panel/orders/migrations -name "*.py" ! -name "__init__.py" -delete
docker-compose exec admin python manage.py makemigrations
docker-compose exec admin python manage.py migrate
```

### 🔜 Что дальше?
## ✅ Реализована пагинация

## ✅ Реализована рассылка с кнопкой

## 🔜 Следующий шаг — добавить платёжный шлюз (Tinkoff или ЮKassa) и экспорт заказов в Excel

# 👨‍💻 Автор
## Станислав Канкин

Telegram: @Stanislav_KRD_89