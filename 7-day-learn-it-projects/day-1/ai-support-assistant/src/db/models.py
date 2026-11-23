from dataclasses import dataclass
import datetime
from nt import error
from typing import Literal

@dataclass
class DocumentRecord:
    doc_id: str
    file_name: str
    path: str
    version: str
    status: Literal["uploaded", "processing", "ready", "failed"]
    uploaded_at: datetime
    processed_at: datetime | None = None
    error_message: str | None = None

