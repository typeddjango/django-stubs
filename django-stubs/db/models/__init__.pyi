from .base import Model as Model

from .fields import (AutoField as AutoField,
                     IntegerField as IntegerField,
                     SmallIntegerField as SmallIntegerField,
                     CharField as CharField,
                     Field as Field,
                     SlugField as SlugField,
                     TextField as TextField)
from .fields.related import (ForeignKey as ForeignKey)
from .deletion import CASCADE as CASCADE
from .query import QuerySet as QuerySet