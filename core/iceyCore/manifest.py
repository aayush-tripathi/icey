from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field


class TerminalPanel(BaseModel):
    cwd: Path
    command_history: List[str] = Field(default_factory=list)
    scrollback: str = ""


class FileState(BaseModel):
    path: Path
    cursor: int = 0
    unsaved_changes: str | None = None


class ContextManifest(BaseModel):
    user_email: str
    git_branch: str
    env_vars: Dict[str, str] = Field(default_factory=dict)
    open_files: List[FileState] = Field(default_factory=list)
    terminals: List[TerminalPanel] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
