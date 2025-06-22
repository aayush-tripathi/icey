from core.iceyCore.manifest import ContextManifest


def test_roundtrip():
    m = ContextManifest(user_email="a@b.com", git_branch="dev")
    assert m.model_validate_json(m.model_dump_json()) == m
