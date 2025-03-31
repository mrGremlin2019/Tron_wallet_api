# Tron Wallet API

Микросервис для получения информации о кошельках в сети Tron и хранения истории запросов.

## 📌 Основные возможности

- Получение информации о кошельке в сети Tron (баланс, энергия, пропускная способность)
- Сохранение истории запросов в базе данных
- Просмотр истории запросов с пагинацией

### 🚀  Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-репозиторий/tron-wallet-api.git
   cd tron-wallet-api
   ```
   
2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

### Запуск
 Запустите сервер:

   ```bash
     uvicorn app.main:app --reload
   ```
API будет доступно по адресу: http://127.0.0.1:8000