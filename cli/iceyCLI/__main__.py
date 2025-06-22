from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from core.iceyCore.crypto.aes import decrypt, encrypt
from core.iceyCore.manifest import ContextManifest
from core.iceyCore.storage.localFS import LocalStore

app = typer.Typer(help="Icey – universal context keeper CLI")

STATE_DIR = Path.home() / ".icey"
store = LocalStore(STATE_DIR)


def _key_required(key: str | None) -> bytes:
    if not key:
        typer.secho("Encryption key required", fg="red", err=True)
        raise typer.Exit(code=1)
    return key.encode()


# Commands:


@app.command()
def create(email: str) -> None:
    """Create a new empty profile."""
    manifest = ContextManifest(user_email=email, git_branch="")
    store.save(manifest)
    print(f"[green]Created profile for {email}")


@app.command()
def save(
    email: str,
    encrypt_flag: bool = typer.Option(
        False, "--encrypt", "-e", help="Encrypt snapshot"
    ),
    key: str | None = typer.Option(None, "--key", help="Fernet key (base64 urlsafe)"),
) -> None:
    """Capture the current context (stub data for Day-1)."""
    manifest = ContextManifest(user_email=email, git_branch="main")
    raw = manifest.model_dump_json(indent=2).encode()
    if encrypt_flag:
        raw = encrypt(raw, _key_required(key))

    store.save_bytes(email, raw)
    print("[green]Context saved")


@app.command()
def load(
    email: str,
    decrypt_flag: bool = typer.Option(
        False, "--decrypt", "-d", help="Decrypt snapshot"
    ),
    key: str | None = typer.Option(None, "--key", help="Fernet key"),
) -> None:
    """Load and print a manifest."""
    raw = store.load_bytes(email)

    if decrypt_flag:
        raw = decrypt(raw, _key_required(key))

    manifest = ContextManifest.model_validate_json(raw.decode())
    print("[bold cyan]Loaded manifest:[/]\n", manifest.model_dump_json(indent=2))


@app.command()
def delete(
    email: str,
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
) -> None:
    """Delete a saved snapshot."""
    if not yes:
        typer.confirm(f"Delete snapshot for {email}?", abort=True)
    store.delete(email)
    print("[yellow]Deleted")
