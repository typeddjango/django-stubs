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
from django.forms.widgets import (
    CheckboxInput,
    ClearableFileInput,
    DateInput,
    DateTimeInput,
    EmailInput,
    NullBooleanSelect,
    NumberInput,
    Select,
    SelectMultiple,
    SplitDateTimeWidget,
    Textarea,
    TextInput,
    TimeInput,
    URLInput,
)
from typing_extensions import assert_type

assert_type(Field.widget, type[TextInput] | TextInput)
assert_type(Field().widget, TextInput)

assert_type(CharField.widget, type[TextInput] | TextInput)
assert_type(CharField().widget, TextInput)

assert_type(IntegerField.widget, type[NumberInput] | NumberInput)
assert_type(IntegerField().widget, NumberInput)

assert_type(FloatField.widget, type[NumberInput] | NumberInput)
assert_type(FloatField().widget, NumberInput)

assert_type(DecimalField.widget, type[NumberInput] | NumberInput)
assert_type(DecimalField().widget, NumberInput)

assert_type(DateField.widget, type[DateInput] | DateInput)
assert_type(DateField().widget, DateInput)

assert_type(TimeField.widget, type[TimeInput] | TimeInput)
assert_type(TimeField().widget, TimeInput)

assert_type(DateTimeField.widget, type[DateTimeInput] | DateTimeInput)
assert_type(DateTimeField().widget, DateTimeInput)

assert_type(DurationField.widget, type[TextInput] | TextInput)
assert_type(DurationField().widget, TextInput)

regex = cast(str, ...)

assert_type(RegexField.widget, type[TextInput] | TextInput)
assert_type(RegexField(regex).widget, TextInput)

assert_type(EmailField.widget, type[EmailInput] | EmailInput)
assert_type(EmailField().widget, EmailInput)

assert_type(FileField.widget, type[ClearableFileInput] | ClearableFileInput)
assert_type(FileField().widget, ClearableFileInput)

assert_type(ImageField.widget, type[ClearableFileInput] | ClearableFileInput)
assert_type(ImageField().widget, ClearableFileInput)

assert_type(URLField.widget, type[URLInput] | URLInput)
assert_type(URLField().widget, URLInput)

assert_type(BooleanField.widget, type[CheckboxInput] | CheckboxInput)
assert_type(BooleanField().widget, CheckboxInput)

assert_type(NullBooleanField.widget, type[NullBooleanSelect] | NullBooleanSelect)
assert_type(NullBooleanField().widget, NullBooleanSelect)

assert_type(ChoiceField.widget, type[Select] | Select)
assert_type(ChoiceField().widget, Select)

assert_type(TypedChoiceField.widget, type[Select] | Select)
assert_type(TypedChoiceField().widget, Select)

assert_type(MultipleChoiceField.widget, type[SelectMultiple] | SelectMultiple)
assert_type(MultipleChoiceField().widget, SelectMultiple)

assert_type(TypedMultipleChoiceField.widget, type[SelectMultiple] | SelectMultiple)
assert_type(TypedMultipleChoiceField().widget, SelectMultiple)

fields = cast(list[Field], ...)

assert_type(ComboField.widget, type[TextInput] | TextInput)
assert_type(ComboField(fields).widget, TextInput)

assert_type(MultiValueField.widget, type[TextInput] | TextInput)
assert_type(MultiValueField(fields).widget, TextInput)

path = cast(str, ...)

assert_type(FilePathField.widget, type[Select] | Select)
assert_type(FilePathField(path).widget, Select)

assert_type(SplitDateTimeField.widget, type[SplitDateTimeWidget] | SplitDateTimeWidget)
assert_type(SplitDateTimeField().widget, SplitDateTimeWidget)

assert_type(GenericIPAddressField.widget, type[TextInput] | TextInput)
assert_type(GenericIPAddressField().widget, TextInput)

assert_type(SlugField.widget, type[TextInput] | TextInput)
assert_type(SlugField().widget, TextInput)

assert_type(UUIDField.widget, type[TextInput] | TextInput)
assert_type(UUIDField().widget, TextInput)

assert_type(JSONField.widget, type[Textarea] | Textarea)
assert_type(JSONField().widget, Textarea)


class CustomIntegerField(IntegerField): ...


assert_type(CustomIntegerField.widget, type[NumberInput] | NumberInput)
assert_type(CustomIntegerField().widget, NumberInput)
