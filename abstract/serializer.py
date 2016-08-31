from rest_framework import serializers


def __dynamic__init__(self, *args, **kwargs):
    """
    참고 링크 - http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields

    __init__ 함수를 오버라이딩 하여 다음과 같이 Serializer instance 생성 시 fields tuple을 인자로 넘기도록 함.
    MySerializer(user, fields=('a', 'b', 'c'))
    a, b, c field 정보만 출력가능
    """
    # Don't pass the 'fields' arg up to the superclass
    fields = kwargs.pop('fields', None)

    # Instantiate the superclass normally
    super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

    if fields is not None:
        # Drop any fields that are not specified in the `fields` argument.
        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)