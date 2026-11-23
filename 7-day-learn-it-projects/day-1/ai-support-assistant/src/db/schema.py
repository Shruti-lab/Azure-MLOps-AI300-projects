# Pydantic schema
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class QueryRequest(BaseModel):
    question: str = Field(...,description="Users question",min_length=1,max_length=1000)

class SourceRef(BaseModel):
    doc_id: str
    file_name: str
    snippet: str

class QueryResponse(BaseModel):
    answer: str = Field(...,description="RAG response")
    sources: list[SourceRef] = Field(...,description="List of sources refered")

# Used while uploading docuemnt
class DocumentInfo(BaseModel):
    doc_id: str
    file_name: str
    status: Literal["uploaded","processing","ready","failed"]
    version: str


class AzureSearchRecord(BaseModel):
    id: str = Field(..., alias="id", description="The strict string Key field for the index")
    content: str = Field(..., description="The searchable text field (LangChain's text_key)")
    content_vector: List[float] = Field(..., description="Collection(Edm.Single) array for vectors")
    
    # Custom metadata fields (flat structure matching Azure index schema)
    source: str
    title: str
    category: str
    rating: Optional[float] = None

# Example mapping an external data packet
record = AzureSearchRecord(
    id="doc_001",
    content="Azure AI Search allows native vectorization.",
    content_vector=[0.012, -0.456, 0.789],
    source="manual.txt",
    title="AI Search Overview",
    category="Cloud Systems"
)
