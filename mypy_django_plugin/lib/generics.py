def make_classes_generic(*klasses: type) -> None:
    for klass in klasses:
        def fake_classgetitem(cls, *args, **kwargs):
            return cls

        klass.__class_getitem__ = classmethod(fake_classgetitem)  # type: ignore
