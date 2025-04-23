from typing import cast

from django.forms.fields import (
    BooleanField,
    CharField,
    ChoiceField,
    ComboField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    EmailField,
    Field,
    FileField,
    FilePathField,
    FloatField,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    JSONField,
    MultipleChoiceField,
    MultiValueField,
    NullBooleanField,
    RegexField,
    SlugField,
    SplitDateTimeField,
    TimeField,
    TypedChoiceField,
    TypedMultipleChoiceField,
    URLField,
    UUIDField,
)
from django.forms.widgets import Widget
from typing_extensions import assert_type

assert_type(CharField.widget, type[Widget] | Widget)
assert_type(CharField().widget, Widget)

assert_type(IntegerField.widget, type[Widget] | Widget)
assert_type(IntegerField().widget, Widget)

assert_type(FloatField.widget, type[Widget] | Widget)
assert_type(FloatField().widget, Widget)

assert_type(DecimalField.widget, type[Widget] | Widget)
assert_type(DecimalField().widget, Widget)

assert_type(DateField.widget, type[Widget] | Widget)
assert_type(DateField().widget, Widget)

assert_type(TimeField.widget, type[Widget] | Widget)
assert_type(TimeField().widget, Widget)

assert_type(DateTimeField.widget, type[Widget] | Widget)
assert_type(DateTimeField().widget, Widget)

assert_type(DurationField.widget, type[Widget] | Widget)
assert_type(DurationField().widget, Widget)

regex = cast(str, ...)

assert_type(RegexField.widget, type[Widget] | Widget)
assert_type(RegexField(regex).widget, Widget)

assert_type(EmailField.widget, type[Widget] | Widget)
assert_type(EmailField().widget, Widget)

assert_type(FileField.widget, type[Widget] | Widget)
assert_type(FileField().widget, Widget)

assert_type(ImageField.widget, type[Widget] | Widget)
assert_type(ImageField().widget, Widget)

assert_type(URLField.widget, type[Widget] | Widget)
assert_type(URLField().widget, Widget)

assert_type(BooleanField.widget, type[Widget] | Widget)
assert_type(BooleanField().widget, Widget)

assert_type(NullBooleanField.widget, type[Widget] | Widget)
assert_type(NullBooleanField().widget, Widget)

assert_type(ChoiceField.widget, type[Widget] | Widget)
assert_type(ChoiceField().widget, Widget)

assert_type(TypedChoiceField.widget, type[Widget] | Widget)
assert_type(TypedChoiceField().widget, Widget)

assert_type(MultipleChoiceField.widget, type[Widget] | Widget)
assert_type(MultipleChoiceField().widget, Widget)

assert_type(TypedMultipleChoiceField.widget, type[Widget] | Widget)
assert_type(TypedMultipleChoiceField().widget, Widget)

fields = cast(list[Field], ...)

assert_type(ComboField.widget, type[Widget] | Widget)
assert_type(ComboField(fields).widget, Widget)

assert_type(MultiValueField.widget, type[Widget] | Widget)
assert_type(MultiValueField(fields).widget, Widget)

path = cast(str, ...)

assert_type(FilePathField.widget, type[Widget] | Widget)
assert_type(FilePathField(path).widget, Widget)

assert_type(SplitDateTimeField.widget, type[Widget] | Widget)
assert_type(SplitDateTimeField().widget, Widget)

assert_type(GenericIPAddressField.widget, type[Widget] | Widget)
assert_type(GenericIPAddressField().widget, Widget)

assert_type(SlugField.widget, type[Widget] | Widget)
assert_type(SlugField().widget, Widget)

assert_type(UUIDField.widget, type[Widget] | Widget)
assert_type(UUIDField().widget, Widget)

assert_type(JSONField.widget, type[Widget] | Widget)
assert_type(JSONField().widget, Widget)
