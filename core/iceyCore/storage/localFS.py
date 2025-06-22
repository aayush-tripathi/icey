from pathlib import Path
from typing import Iterable

from core.iceyCore.manifest import ContextManifest


class LocalStore:
    """
    Save / load manifests as JSON files
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.home() / ".icey"
        self.root.mkdir(exist_ok=True)

    def _path(self, email: str) -> Path:
        return self.root / f"{email}.json"

    def save_bytes(self, email: str, data: bytes) -> Path:
        p = self._path(email)
        p.write_bytes(data)
        return p

    def save(self, manifest: ContextManifest) -> Path:
        return self.save_bytes(
            manifest.user_email, manifest.model_dump_json(indent=2).encode()
        )

    def load_bytes(self, email: str) -> bytes:
        return self._path(email).read_bytes()

    def load(self, email: str) -> ContextManifest:
        return ContextManifest.model_validate_json(self.load_bytes(email).decode())

    def delete(self, email: str) -> None:
        self._path(email).unlink(missing_ok=True)

    def list_profiles(self) -> Iterable[str]:
        yield from (p.stem for p in self.root.glob("*.json"))
