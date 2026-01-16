from django.db.models import F, Value
from django.db.models.functions import Lag, Lead, NthValue

Lag("field")
Lag(F("field"))
Lead("field")
Lead(F("field"))
NthValue("field", nth=2)
NthValue(F("field"), nth=2)

Lag("field", default=42)
Lag("field", default="string")
Lag("field", default=Value("value"))
Lag("field", default=F("other"))
