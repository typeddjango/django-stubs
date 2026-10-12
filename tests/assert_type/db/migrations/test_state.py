from django.db.migrations.state import ProjectState


state = ProjectState()
model_keys: set[tuple[str, str]] = set()
state.reload_models(model_keys)
