# -*- coding: utf-8 -*-

import config
from metagraph.processor import *

class Loader:

    """
    Класс для загрузки ситуаций и проверки загрузки
    """

    example_vertex_name_1 = "Пример 1"
    example_vertex_name_2 = "Пример 2"

    @staticmethod
    def load():
        """
        Загрузка в модель тестовых данных
        """
        metagraphModelConfig = MetagraphModelConfig(config.mongo_db, config.mongo_collection)
        proc = MetagraphModelProcessor(metagraphModelConfig)
        proc.drop_db()
        Loader.load_examples(proc)

    @staticmethod
    def load_examples(proc: MetagraphModelProcessor):
        """
        Загрузка примеров
        """

        # Пример 1 (соответствует рисунку 4 в статье)
        # James noted that Paul noted at 4 p.m. that John arrived in London

        john = proc.create_vertex("Джон")
        london = proc.create_vertex("Лондон")
        arrived = proc.create_edge("прибыл", john, london)

        situation_1 = proc.create_vertex("Ситуация_1")
        situation_1.Vertices = [john, london]
        situation_1.Edges = [arrived]
        situation_1.save()

        paul = proc.create_vertex("Пол")
        noted_sit_1 = proc.create_edge("отметил", paul, situation_1)
        noted_sit_1.add_attr(AttributeString(name="время", value="16:00"))

        situation_2 = proc.create_vertex("Ситуация_2")
        situation_2.Vertices = [paul, situation_1]
        situation_2.Edges = [noted_sit_1]
        situation_2.add_attr(AttributeString(name="время", value="16:00"))

        james = proc.create_vertex("Джеймс")
        noted_sit_2 = proc.create_edge("отметил", james, situation_2)

        situation_3 = proc.create_vertex("Ситуация_3")
        situation_3.Vertices = [james, situation_2]
        situation_3.Edges = [noted_sit_2]
        situation_3.save()

        example_1 = proc.create_vertex(Loader.example_vertex_name_1)
        example_1.Vertices = [situation_3]
        example_1.save()

        # Пример 2 (соответствует рисунку 7 в статье)
        # John arrived to London at 4 p.m. by train
        # in order to meet his classmates James and Paul

        classmates = proc.create_vertex("одноклассники")
        classmates.Vertices = [james, paul]
        classmates.save()

        living = proc.create_edge("живущие", classmates, london)
        meet = proc.create_edge("встретиться", john, classmates)

        arrived_2 = proc.create_edge("прибыл", john, london)
        arrived_2.add_attr(AttributeString(name="время", value="16:00"))
        arrived_2.add_attr(AttributeString(name="транспорт", value="поезд"))

        example_2 = proc.create_vertex(Loader.example_vertex_name_2)
        example_2.Vertices = [john, london, classmates]
        example_2.Edges = [living, meet, arrived_2]
        example_2.save()


    @staticmethod
    def check_load():
        """
        проверка загрузки данных
        """
        level = 0
        separator = "*" * 100
        metagraphModelConfig = MetagraphModelConfig(config.mongo_db, config.mongo_collection)
        proc = MetagraphModelProcessor(metagraphModelConfig)
        proc.first_vertex_by_name(Loader.example_vertex_name_1).print_recursive(level)
        print(separator)
        proc.first_vertex_by_name(Loader.example_vertex_name_2).print_recursive(level)


if __name__ == '__main__':
    Loader.load()
    Loader.check_load()