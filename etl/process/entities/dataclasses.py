from dataclasses import dataclass, field
from zoneinfo import ZoneInfo
from datetime import datetime
from typing import Union
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class PersonProduced:
    id: UUID = field(default_factory=uuid4)
    modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

        if isinstance(self.modified, str):
            self.modified = datetime.fromisoformat(self.modified).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )


@dataclass(kw_only=True)
class FilmworkEnricher:
    id: UUID = field(default_factory=uuid4)
    modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

        if isinstance(self.modified, str):
            self.modified = datetime.fromisoformat(self.modified).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )

class FilworkPerson:
    person_id: str
    person_name: str
    person_role: str


@dataclass(kw_only=True)
class FilmWork:
    id: UUID = field(default_factory=uuid4)
    title: str
    description: str
    rating: float
    type: str
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    persons: list[FilworkPerson]
    genres:list[str]

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

        if isinstance(self.created, str):
            self.created = datetime.fromisoformat(self.created).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )

        if isinstance(self.modified, str):
            self.modified = datetime.fromisoformat(self.modified).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )


@dataclass(kw_only=True)
class Person:
    id: UUID = field(default_factory=uuid4)
    full_name: str
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

        if isinstance(self.created, str):
            self.created = datetime.fromisoformat(self.created).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )

        if isinstance(self.modified, str):
            self.modified = datetime.fromisoformat(self.modified).replace(
                tzinfo=ZoneInfo("Etc/UTC")
            )
