"""Process runner protocols and default implementations."""

from __future__ import annotations

import asyncio
import subprocess
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class SyncProcess(Protocol):
    """Protocol for synchronous process handles."""

    returncode: int | None

    def communicate(self, timeout: float | None = None) -> tuple[str, str]:
        ...

    def terminate(self) -> None:
        ...

    def kill(self) -> None:
        ...

    def wait(self, timeout: float | None = None) -> int:
        ...


@runtime_checkable
class SyncProcessRunner(Protocol):
    """Protocol for spawning synchronous processes."""

    def spawn(self, command: list[str], *, cwd: str | None = None) -> SyncProcess:
        ...


@dataclass
class SubprocessRunner:
    """Default runner using subprocess.Popen."""

    def spawn(self, command: list[str], *, cwd: str | None = None) -> subprocess.Popen[str]:
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
        )


@runtime_checkable
class AsyncProcess(Protocol):
    """Protocol for asynchronous process handles."""

    stdout: asyncio.StreamReader | None
    returncode: int | None

    async def wait(self) -> int:
        ...

    def terminate(self) -> None:
        ...


@runtime_checkable
class AsyncProcessRunner(Protocol):
    """Protocol for spawning asynchronous processes."""

    async def spawn(self, command: str) -> AsyncProcess:
        ...


@dataclass
class AsyncSubprocessRunner:
    """Default async runner using asyncio subprocess shell."""

    async def spawn(self, command: str) -> asyncio.subprocess.Process:
        return await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
