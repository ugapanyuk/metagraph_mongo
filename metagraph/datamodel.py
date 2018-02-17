# -*- coding: utf-8 -*-

from mongoengine import *
from asq.initiators import *
from metagraph.data_helper import DataHelper

"""
Метаграфовая модель данных, реализованная в mongodb с использованием mongoengine
"""

class AttributeGeneric(EmbeddedDocument):
    name = StringField()
    meta = {'allow_inheritance': True}


class VertexGeneric(Document):
    meta = {'allow_inheritance': True}
    name = StringField()
    Attributes = EmbeddedDocumentListField(AttributeGeneric)

    def add_attr(self, new_attr: AttributeGeneric):
        attr_temp = []
        if len(self.Attributes) > 0:
            attr_temp = self.Attributes
        attr_temp.append(new_attr)
        self.Attributes = attr_temp
        self.save()


class AttributeString(AttributeGeneric):
    value = StringField()


class AttributeStringList(AttributeGeneric):
    value = ListField(StringField())


class AttributeBoolean(AttributeGeneric):
    value = BooleanField()


class AttributeInt(AttributeGeneric):
    value = LongField()


class AttributeFloat(AttributeGeneric):
    value = FloatField()


class AttributeRef(AttributeGeneric):
    value = ReferenceField(VertexGeneric)


class Edge(VertexGeneric):
    s = ReferenceField(VertexGeneric)
    d = ReferenceField(VertexGeneric)

    def __str__(self):
        return 'Связь: ' + self.name + ' (' + self.s.name + ' -> ' + self.d.name + ')'


class Vertex(VertexGeneric):
    Vertices = ListField(ReferenceField(VertexGeneric))
    Edges = ListField(ReferenceField(Edge))

    def __str__(self):
        return 'Вершина: ' + self.name

    def print_recursive(self, level: int):
        """
        Рекурсивная печать информации о вершине, вложеннных вершинах, атрибутах, связях
        """
        DataHelper.PrintWithLevel(str(self), level)

        if len(self.Attributes) > 0:
            DataHelper.PrintWithLevel("Вложенные атрибуты: ", level + 1)
            for attr in self.Attributes:
                attr_str = attr.name + ' = ' + str(attr.value)
                DataHelper.PrintWithLevel(attr_str, level + 2)

        if len(self.Vertices) > 0:
            DataHelper.PrintWithLevel("Вложенные вершины: ", level + 1)
            for v in self.Vertices:
                v.print_recursive(level + 2)

        if len(self.Edges) > 0:
            DataHelper.PrintWithLevel("Вложенные связи: ", level + 1)
            for edge in self.Edges:
                DataHelper.PrintWithLevel(str(edge), level + 2)
                if len(edge.Attributes) > 0:
                    DataHelper.PrintWithLevel("Вложенные атрибуты: ", level + 3)
                    for edge_attr in edge.Attributes:
                        edge_attr_str = edge_attr.name + ' = ' + str(edge_attr.value)
                        DataHelper.PrintWithLevel(edge_attr_str, level + 4)



    def attribute_by_name(self, attr_name):
        for attr in self.Attributes:
            if attr.name == attr_name:
                return attr.value
        return None

    def attribute_obj_by_name(self, attr_name):
        for attr in self.Attributes:
            if attr.name == attr_name:
                return attr
        return None

    def has_attribute(self, attr_name):
        res = self.attribute_by_name(attr_name)
        if res is None:
            return False
        else:
            return True

    def delete_attribute(self, attr_name):
        old_attrs = list(self.Attributes)
        new_attrs = []
        for attr in old_attrs:
            if attr.name != attr_name:
                new_attrs.append(attr)
        self.Attributes = new_attrs
        self.save()

    def first_subvertex_by_name(self, name_param):
        for v in self.Vertices:
            if v.name == name_param:
                return v
        return None


