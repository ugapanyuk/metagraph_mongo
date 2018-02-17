# metagraph_mongo - реализация метаграфового хранилища с помощью mongodb

## Для работы необходимо установить:

- mongodb - https://www.mongodb.com/ (пожалуйста не забудьте создать каталог для данных /data/db и запустить службу mongo перед запуском проекта)
- mongoengine - http://mongoengine.org/ аналог ORM для mongo
- asq - https://github.com/sixty-north/asq аналог LINQ для Python

Проект тестировался под Python 3.6

В каталоге paper находится черновая версия статьи, примеры из которой реализованы в тесте.

Для создания примеров метагарфов необходимо использовать /tests/test_create_metagraph.py

