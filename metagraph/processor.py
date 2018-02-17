# -*- coding: utf-8 -*-

from mongoengine import *
from asq.initiators import *
from metagraph.configuration import *
from metagraph.datamodel import *

class MetagraphModelProcessor:
    """
    Класс для обработки метаграфовой модели
    """
    metagraphModelConfig = None
    db = None

    def __init__(self , metagraph_model_config_param):
        """
        Конструктор класса
        :type metagraph_model_config_param: MetagraphModelConfig
        """
        self.metagraphModelConfig = metagraph_model_config_param
        self.db = connect(self.metagraphModelConfig.db_name)

    def create_vertex(self, vertex_name: str) -> Vertex:
        """
        Добавление вершины
        """
        v = Vertex(name=vertex_name)
        v.save()
        return v

    def create_edge(self, edge_name: str, src: Vertex, dest: Vertex) -> Edge:
        """
        Добавление связи
        """
        e = Edge(name=edge_name)
        e.s = src
        e.d = dest
        e.save()
        return e

    def drop_db(self):
        try:
            self.db.drop_database(self.metagraphModelConfig.db_name)
        except Exception:
            pass

    def vertices_by_name(self, name_param: str):
        """
        Список всех вершин с заданным именем
        """
        vs = Vertex.objects(name=name_param).all()
        return vs

    def first_vertex_by_name(self, name_param: str):
        """
        Вершина с заданным именем (предполагается что имя уникальное)
        """
        vs = self.vertices_by_name(name_param)
        if len(vs) > 0:
            return vs[0]
        else:
            return None


