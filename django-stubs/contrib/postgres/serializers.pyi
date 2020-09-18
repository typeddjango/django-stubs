from django.db.migrations.serializer import BaseSerializer as BaseSerializer

class RangeSerializer(BaseSerializer):
    def serialize(self): ...
