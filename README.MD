# FastAPI Image Moderation Service

Тестовое задание:
Сервис для модерации изображений с использованием DeepAI NSFW Detector API. Проверяет изображения на наличие NSFW-контента и возвращает результат анализа.

## Особенности

- Проверка изображений из папки `images`
- Поддержка форматов JPG и PNG
- Оценка NSFW-контента с порогом 0.7
- Детальные сообщения об ошибках
- Асинхронная обработка файлов

## Требования

- Python 3.10+
- Установленные зависимости из `requirements.txt`

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/jforsety/test_ai_moderate.git
cd test_ai_moderate
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Переименуйте файл .env_prod в корне проекта на .env и замените содержимое:
```bash
DEEPAI_API_KEY=ваш API ключ
URL=url для post запроса
```
5. Запустите приложение:
```bash
python main.py
```
Сервис будет доступен по адресу: http://127.0.0.1:8000

В папке images уже есть тестовое изображение, можно добавить свое.

## Использование через Postman

### Пример запроса
Endpoint:
```commandline
POST http://localhost:8000/moderate
```
Headers:
```commandline
Content-Type: application/json
```
Body (raw JSON):
```commandline
{
    "filename": "test.jpg"
}
```
### Примеры ответов
Успешная модерация:
```commandline
{
    "status": "OK",
    "score": 0.21
}
```
Обнаружен NSFW-контент:
```commandline
{
    "status": "REJECTED",
    "reason": "Обнаружен NSFW контент",
    "score": 0.89
}
```
Ошибка (файл не найден):
```commandline
{
    "detail": "Файл не найден"
}
```
Неподдерживаемый формат:
```commandline
{
    "detail": "Поддерживаются только JPG и PNG"
}
```
Ошибка на стороне DeepAI:
```commandline
{
    "status": "ERROR",
    "reason": "Ошибка DeepAI"
}
```
## Структура проекта
```commandline
.
├── images/              # Папка с изображениями для анализа
├── venv/                # Виртуальное окружение (генерируется)
├── .env                 # Файл с переменными окружения
├── main.py              # Основной код приложения
├── requirements.txt     # Зависимости
└── README.md            # Документация
```
## Настройка окружения
Перед запуском необходимо получить API-ключ от DeepAI:
```commandline
Зарегистрируйтесь на https://deepai.org/

Получите API-ключ в личном кабинете

Добавьте ключ в файл .env как DEEPAI_API_KEY
```
## Тестирование
Для тестирования можно использовать изображения:

Безопасное изображение: любое нейтральное фото

NSFW-контент: изображения с откровенным содержанием

Рекомендуемые тестовые изображения можно найти на специализированных ресурсах для тестирования контент-фильтров.
