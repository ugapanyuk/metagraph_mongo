# -*- coding: utf-8 -*-

class MetagraphModelConfig:
    """
    Класс для подключения к БД
    """
    db_name = ''
    collection_name = ''
    def __init__(self, db_param, collection_param):
         self.db_name = db_param
         self.collection_name = collection_param