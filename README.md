# Wallet save

Данный сервис позволяет сохранять расходы, мониторить их, смотреть статистику в личном кабинете. Также далее будет добавляться дополнительный функционал и интеграция с telegram.

*Backend*: FastAPI  
*Frontend*: React

Для **dev** используется *асинхронная sqlite*.

**TODO**:
- [ ] Внедрение парсинга расходов (Выгрузка из банка)
- [ ] Внедрение методов машинного обучения
	- [ ] Предсказание следующих трат
	- [ ] Оптимизация затрат по категориям  

Методы *API* можно посмотреть при развертвании бекенда по ссылке http://127.0.0.1:8000/docs или http://localhost:8000/docs.  
Регистрация нового пользователя пока вручную со стороны администратора по пути http://localhost:8000/docs#/auth/register_register_dev_register_post.  
Веб-интерфейс находиться по пути http://localhost:3000 или http://127.0.0.1:3000.

----

## Запуск
Инициализация:
```bash
git clone https://github.com/s1lver29/wallet-save.git
cd wallet-save/docker
echo "BRANCH=main" >> .env
echo "PORT_FRONTEND=3000" >> .env
echo "PORT_BACKEND=8000" >> .env
```
Запуск:
```bash
docker compose up --build
```
