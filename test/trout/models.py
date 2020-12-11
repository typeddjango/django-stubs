from datetime import time, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Union
from uuid import UUID

from django.contrib.postgres.fields import (
    ArrayField,
    CICharField,
    CIEmailField,
    CITextField,
    HStoreField,
    JSONField,
)
from django.db import models
from django.db.models.manager import RelatedManager


class User(models.Model):

    pass


class Post(models.Model):

    pass


class PostToComment(models.Model):
    pass


class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    post_fk = models.ForeignKey(
        Post, on_delete=models.CASCADE, help_text="Comment for a post."
    )
    post_fk_nullable = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, help_text="Comment for a post."
    )

    post_one_to_one = models.OneToOneField(Post, on_delete=models.CASCADE)
    post_one_to_one_nullable = models.OneToOneField(
        Post, null=True, on_delete=models.CASCADE
    )

    post_many_to_many = models.ManyToManyField(Post, through=PostToComment)
    post_many_to_many_nullable = models.ManyToManyField(
        Post, through=PostToComment, null=True
    )

    created_at = models.DateTimeField()
    created_at_nullable = models.DateTimeField(null=True)

    created_at_date = models.DateField()
    created_at_date_nullable = models.DateField(null=True)

    char = models.CharField()
    char_nullable = models.CharField(null=True)

    text = models.TextField()
    text_nullable = models.TextField(null=True)
    test_with_explicit_null_false = models.TextField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        help_text="",
    )

    integer = models.IntegerField()
    integer_nullable = models.IntegerField(null=True)

    float = models.FloatField()
    float_nullable = models.FloatField(null=True)

    uuid = models.UUIDField()
    uuid_nullable = models.UUIDField(null=True)

    url = models.URLField()
    url_nullable = models.URLField(null=True)

    email = models.EmailField()
    email_nullable = models.EmailField(null=True)

    decimal = models.DecimalField()
    decimal_nullable = models.DecimalField(null=True)

    bool = models.BooleanField()
    bool_nullable = models.BooleanField(null=True)

    ip_address = models.IPAddressField()
    ip_address_nullable = models.IPAddressField(null=True)

    generic_ip_address = models.GenericIPAddressField()
    generic_ip_address_nullable = models.GenericIPAddressField(null=True)

    time = models.TimeField()
    time_nullable = models.TimeField(null=True)

    file_path = models.FilePathField()
    file_path_nullable = models.FilePathField(null=True)

    binary = models.BinaryField()
    binary_nullable = models.BinaryField(null=True)

    duration = models.DurationField()
    duration_nullable = models.DurationField(null=True)

    slug = models.SlugField()
    slug_nullable = models.SlugField(null=True)

    pos_int = models.PositiveIntegerField()
    pos_int_nullable = models.PositiveIntegerField(null=True)

    pos_small_int = models.PositiveSmallIntegerField()
    pos_small_int_nullable = models.PositiveSmallIntegerField(null=True)

    small_int = models.SmallIntegerField()
    small_int_nullable = models.SmallIntegerField(null=True)

    big_int = models.BigIntegerField()
    big_int_nullable = models.BigIntegerField(null=True)

    ci_text = CITextField()
    ci_text_nullable = CITextField(null=True)

    ci_char = CICharField()
    ci_char_nullable = CICharField(null=True)

    ci_email = CIEmailField()
    ci_email_nullable = CIEmailField(null=True)

    hstore = HStoreField()
    hstore_nullable = HStoreField(null=True)

    array = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8,
    )
    array_nullable = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8,
        null=True,
    )

    created_by = models.ForeignKey["User"](
        "User", on_delete=models.CASCADE, help_text="owner of the comment"
    )

    user_type = models.ForeignKey(User, on_delete=models.CASCADE)
    user_str = models.ForeignKey("User", on_delete=models.CASCADE)  # type: ignore [var-annotated]
    nullable_user_type = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nullable_user_str = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    not_nullable_user_str = models.ForeignKey(  # type: ignore [var-annotated]
        "User", on_delete=models.CASCADE, null=False
    )
    null_str_specified = models.ForeignKey["User"](
        "User", on_delete=models.CASCADE, null=True
    )

    metadata = JSONField()


def process_non_nullable(
    x: Union[
        Post,
        User,
        time,
        float,
        bytes,
        UUID,
        int,
        str,
        Decimal,
        timedelta,
        List[object],
        Dict[str, Optional[str]],
    ]
) -> None:
    ...


def main() -> None:

    post = Post()

    print(post.id)  # type: ignore [attr-defined]

    comment = Comment()
    comment.save()

    # Django way to duplicate an instance
    comment.id = None
    comment.save()

    print(comment.id)

    process_non_nullable(comment.post_fk)
    if isinstance(comment.post_fk_nullable, type(None)):
        print(comment.post_fk_nullable)
    if comment.post_fk_nullable is not None:
        print(comment.post_fk_nullable)
    if not isinstance(comment.post_fk, Post):
        print()  # type: ignore [unreachable]
    if not comment.post_fk and not isinstance(comment.post_fk, Post):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.post_one_to_one)
    if isinstance(comment.post_one_to_one_nullable, type(None)):
        print(comment.post_one_to_one_nullable)
    if comment.post_one_to_one_nullable is not None:
        print(comment.post_one_to_one_nullable)
    if not isinstance(comment.post_one_to_one, Post):
        print()  # type: ignore [unreachable]
    if not comment.post_one_to_one and not isinstance(comment.post_one_to_one, Post):
        print()  # type: ignore [unreachable]

    # many to many is complicated so we don't check nullability like we do with other fields
    if comment.post_many_to_many_nullable is not None:
        print(comment.post_many_to_many_nullable)
    if not isinstance(comment.post_many_to_many, RelatedManager):
        print()  # type: ignore [unreachable]
    if not comment.post_many_to_many and not isinstance(
        comment.post_many_to_many, RelatedManager
    ):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.text)
    if isinstance(comment.text_nullable, type(None)):
        print(comment.text_nullable)
    if comment.text_nullable is not None:
        print(comment.text_nullable)
    if not isinstance(comment.text, str):
        print()  # type: ignore [unreachable]
    if not comment.text and not isinstance(comment.text, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.integer)
    if isinstance(comment.integer_nullable, type(None)):
        print(comment.integer_nullable)
    if comment.integer_nullable is not None:
        print(comment.integer_nullable)
    if not isinstance(comment.integer, int):
        print()  # type: ignore [unreachable]
    if not comment.integer and not isinstance(comment.integer, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.float)
    if isinstance(comment.float_nullable, type(None)):
        print(comment.float_nullable)
    if comment.float_nullable is not None:
        print(comment.float_nullable)
    if not isinstance(comment.float, float):
        print()  # type: ignore [unreachable]
    if not comment.float and not isinstance(comment.float, float):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.uuid)
    if isinstance(comment.uuid_nullable, type(None)):
        print(comment.uuid_nullable)
    if comment.uuid_nullable is not None:
        print(comment.uuid_nullable)
    if not isinstance(comment.uuid, UUID):
        print()  # type: ignore [unreachable]
    if not comment.uuid and not isinstance(comment.uuid, UUID):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.url)
    if isinstance(comment.url_nullable, type(None)):
        print(comment.url_nullable)
    if comment.url_nullable is not None:
        print(comment.url_nullable)
    if not isinstance(comment.url, str):
        print()  # type: ignore [unreachable]
    if not comment.url and not isinstance(comment.url, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.email)
    if isinstance(comment.email_nullable, type(None)):
        print(comment.email_nullable)
    if comment.email_nullable is not None:
        print(comment.email_nullable)
    if not isinstance(comment.email, str):
        print()  # type: ignore [unreachable]
    if not comment.email and not isinstance(comment.email, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.decimal)
    if isinstance(comment.decimal_nullable, type(None)):
        print(comment.decimal_nullable)
    if comment.decimal_nullable is not None:
        print(comment.decimal_nullable)
    if not isinstance(comment.decimal, Decimal):
        print()  # type: ignore [unreachable]
    if not comment.decimal and not isinstance(comment.decimal, Decimal):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.bool)
    if isinstance(comment.bool_nullable, type(None)):
        print(comment.bool_nullable)
    if comment.bool_nullable is not None:
        print(comment.bool_nullable)
    if not isinstance(comment.bool, int):
        print()  # type: ignore [unreachable]
    if not comment.bool and not isinstance(comment.bool, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.ip_address)
    if isinstance(comment.ip_address_nullable, type(None)):
        print(comment.ip_address_nullable)
    if comment.ip_address_nullable is not None:
        print(comment.ip_address_nullable)
    if not isinstance(comment.ip_address, str):
        print()  # type: ignore [unreachable]
    if not comment.ip_address and not isinstance(comment.ip_address, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.generic_ip_address)
    if isinstance(comment.generic_ip_address_nullable, type(None)):
        print(comment.generic_ip_address_nullable)
    if comment.generic_ip_address_nullable is not None:
        print(comment.generic_ip_address_nullable)
    if not isinstance(comment.generic_ip_address, str):
        print()  # type: ignore [unreachable]
    if not comment.generic_ip_address and not isinstance(
        comment.generic_ip_address, str
    ):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.time)
    if isinstance(comment.time_nullable, type(None)):
        print(comment.time_nullable)
    if comment.time_nullable is not None:
        print(comment.time_nullable)
    if not isinstance(comment.time, time):
        print()  # type: ignore [unreachable]
    if not comment.time and not isinstance(comment.time, time):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.file_path)
    if isinstance(comment.file_path_nullable, type(None)):
        print(comment.file_path_nullable)
    if comment.file_path_nullable is not None:
        print(comment.file_path_nullable)
    if not isinstance(comment.file_path, str):
        print()  # type: ignore [unreachable]
    if not comment.file_path and not isinstance(comment.file_path, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.binary)
    if isinstance(comment.binary_nullable, type(None)):
        print(comment.binary_nullable)
    if comment.binary_nullable is not None:
        print(comment.binary_nullable)
    if not isinstance(comment.binary, bytes):
        print()  # type: ignore [unreachable]
    if not comment.binary and not isinstance(comment.binary, bytes):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.duration)
    if isinstance(comment.duration_nullable, type(None)):
        print(comment.duration_nullable)
    if comment.duration_nullable is not None:
        print(comment.duration_nullable)
    if not isinstance(comment.duration, timedelta):
        print()  # type: ignore [unreachable]
    if not comment.duration and not isinstance(comment.duration, timedelta):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.slug)
    if isinstance(comment.slug_nullable, type(None)):
        print(comment.slug_nullable)
    if comment.slug_nullable is not None:
        print(comment.slug_nullable)
    if not isinstance(comment.slug, str):
        print()  # type: ignore [unreachable]
    if not comment.slug and not isinstance(comment.slug, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.pos_int)
    if isinstance(comment.pos_int_nullable, type(None)):
        print(comment.pos_int_nullable)
    if comment.pos_int_nullable is not None:
        print(comment.pos_int_nullable)
    if not isinstance(comment.pos_int, int):
        print()  # type: ignore [unreachable]
    if not comment.pos_int and not isinstance(comment.pos_int, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.pos_small_int)
    if isinstance(comment.pos_small_int_nullable, type(None)):
        print(comment.pos_small_int_nullable)
    if comment.pos_small_int_nullable is not None:
        print(comment.pos_small_int_nullable)
    if not isinstance(comment.pos_small_int, int):
        print()  # type: ignore [unreachable]
    if not comment.pos_small_int and not isinstance(comment.pos_small_int, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.small_int)
    if isinstance(comment.small_int_nullable, type(None)):
        print(comment.small_int_nullable)
    if comment.small_int_nullable is not None:
        print(comment.small_int_nullable)
    if not isinstance(comment.small_int, int):
        print()  # type: ignore [unreachable]
    if not comment.small_int and not isinstance(comment.small_int, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.big_int)
    if isinstance(comment.big_int_nullable, type(None)):
        print(comment.big_int_nullable)
    if comment.big_int_nullable is not None:
        print(comment.big_int_nullable)
    if not isinstance(comment.big_int, int):
        print()  # type: ignore [unreachable]
    if not comment.big_int and not isinstance(comment.big_int, int):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.ci_text)
    if isinstance(comment.ci_text_nullable, type(None)):
        print(comment.ci_text_nullable)
    if comment.ci_text_nullable is not None:
        print(comment.ci_text_nullable)
    if not isinstance(comment.ci_text, str):
        print()  # type: ignore [unreachable]
    if not comment.ci_text and not isinstance(comment.ci_text, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.ci_char)
    if isinstance(comment.ci_char_nullable, type(None)):
        print(comment.ci_char_nullable)
    if comment.ci_char_nullable is not None:
        print(comment.ci_char_nullable)
    if not isinstance(comment.ci_char, str):
        print()  # type: ignore [unreachable]
    if not comment.ci_char and not isinstance(comment.ci_char, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.ci_email)
    if isinstance(comment.ci_email_nullable, type(None)):
        print(comment.ci_email_nullable)
    if comment.ci_email_nullable is not None:
        print(comment.ci_email_nullable)
    if not isinstance(comment.ci_email, str):
        print()  # type: ignore [unreachable]
    if not comment.ci_email and not isinstance(comment.ci_email, str):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.hstore)
    if isinstance(comment.hstore_nullable, type(None)):
        print(comment.hstore_nullable)
    if comment.hstore_nullable is not None:
        print(comment.hstore_nullable)
    # refinement doesn't work
    # see: https://github.com/python/mypy/issues/9783
    # if not isinstance(comment.hstore, dict):
    #     print()  # type: ignore [unreachable]
    # if not comment.hstore and not isinstance(comment.hstore, dict):
    #     print()  # type: ignore [unreachable]

    process_non_nullable(comment.array)
    if isinstance(comment.array_nullable, type(None)):
        print(comment.array_nullable)
    if comment.array_nullable is not None:
        print(comment.array_nullable)
    if not isinstance(comment.array, list):
        print()  # type: ignore [unreachable]
    if not comment.array and not isinstance(comment.array, list):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.user_type)
    if isinstance(comment.nullable_user_type, type(None)):
        print(comment.nullable_user_type)
    if comment.nullable_user_type is not None:
        process_non_nullable(comment.nullable_user_type)
    if not isinstance(comment.user_type, User):
        print()  # type: ignore [unreachable]

    process_non_nullable(comment.user_str)
    if isinstance(comment.nullable_user_str, type(None)):
        print(comment.nullable_user_str)
    if comment.nullable_user_str is not None:
        print(comment.nullable_user_str)  # type: ignore [unreachable]

    if isinstance(comment.not_nullable_user_str, type(None)):
        print(comment.not_nullable_user_str)
    if comment.not_nullable_user_str is not None:
        print(comment.not_nullable_user_str)

    # if it's T, instead of the expected Optional[T], then will fail to type
    # check
    if isinstance(comment.null_str_specified, type(None)):
        print(comment.null_str_specified)
    if comment.null_str_specified is not None:
        print(comment.null_str_specified)
