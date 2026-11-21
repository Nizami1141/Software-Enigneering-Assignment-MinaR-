from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class ReportInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    sector_name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=80)
    ] = Field(alias="sectorName")
    summary: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=10, max_length=500)
    ]
    status: Literal["draft", "submitted", "reviewed"]


class Report(ReportInput):
    id: str
    owner_id: str = Field(alias="ownerId")
