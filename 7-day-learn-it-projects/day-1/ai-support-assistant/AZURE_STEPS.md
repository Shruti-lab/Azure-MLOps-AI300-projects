# Azure Setup and Deployment Steps

This guide creates the first development environment through the Azure Portal
UI. It does not use Azure CLI, Bicep, Terraform, or DeepEval. Portal labels can
change slightly over time, and some Azure OpenAI models or regions require
approval, quota, or availability checks.

## 1. Prepare Names and Region

Choose one Azure region where Azure Functions, Azure AI Search, Azure OpenAI,
and the models you need are available. Use the same region where possible to
reduce latency and data transfer.

Use these names for development:

```text
Resource group:       rg-ai-support-dev
Storage account:       staisupportdev<unique>
Function App:          func-ai-support-dev-<unique>
Event Grid topic:      evg-ai-support-dev
AI Search:             srch-ai-support-dev-<unique>
Azure OpenAI:          aoai-ai-support-dev
Key Vault:             kv-ai-support-dev-<unique>
Log Analytics:         law-ai-support-dev
Application Insights: appi-ai-support-dev
```

Replace `<unique>` with lowercase letters and numbers. Azure Storage, Azure AI
Search, Function App, and Key Vault names must be globally unique where the
Portal requires it.

## 2. Create the Resource Group

1. Open [portal.azure.com](https://portal.azure.com).
2. Search for **Resource groups**.
3. Select **Create**.
4. Select the correct subscription.
5. Enter `rg-ai-support-dev` as the resource group name.
6. Select the chosen region.
7. Select **Review + create**, then **Create**.

Keep all development resources in this group so they can be managed and
removed together.

## 3. Create Storage for Original Documents

1. In the Portal, search for **Storage accounts** and select **Create**.
2. Select the subscription and `rg-ai-support-dev`.
3. Enter `staisupportdev<unique>` as the storage account name.
4. Select **Standard** performance and **Locally-redundant storage (LRS)** for
   the initial development environment.
5. Keep public access disabled unless the application specifically requires it.
6. On **Data protection**, enable soft delete for blobs if available.
7. Select **Review + create**, then **Create**.
8. Open the storage account and go to **Data storage > Containers**.
9. Create a private container named `documents`.
10. Create a private container named `processed`.

The application writes original uploads to `documents`. It may write extracted
text and chunk backups to `processed`.

## 4. Create Log Analytics and Application Insights

1. Search for **Log Analytics workspaces** and select **Create**.
2. Select `rg-ai-support-dev` and create `law-ai-support-dev`.
3. Search for **Application Insights** and select **Create**.
4. Select **Workspace-based** as the resource mode when shown.
5. Select `rg-ai-support-dev`, name the resource `appi-ai-support-dev`, and
   choose `law-ai-support-dev` as the workspace.
6. Select **Review + create**, then **Create**.

Record the Application Insights connection string only in Azure configuration
or Key Vault. Do not commit it to the repository.

## 5. Create Azure AI Search

1. Search for **Azure AI Search** and select **Create**.
2. Select `rg-ai-support-dev`.
3. Enter `srch-ai-support-dev-<unique>` as the service name.
4. Select the same region as the storage account where possible.
5. Choose the lowest tier that supports your development workload.
6. Leave authentication available for the initial setup, but plan to use a
   managed identity for the deployed Function App.
7. Select **Review + create**, then **Create**.

After the service is created, create an index named `support-chunks`. The index
should contain:

```text
chunk_id       key field, Edm.String
document_id    filterable Edm.String
content        searchable Edm.String
contentVector  vector field with the embedding model dimensions
file_name      searchable/filterable Edm.String
blob_path      retrievable Edm.String
page_number    filterable Edm.Int32, when available
version        filterable Edm.String
```

The exact vector dimension must match the embedding model deployment. Define
the index in code or an import wizard once the model choice is fixed; do not
guess the dimension.

## 6. Create Azure OpenAI and Model Deployments

1. Search for **Azure OpenAI** or **Azure OpenAI Service** in the Portal.
2. Select **Create**.
3. Select `rg-ai-support-dev`, choose the same region where available, and name
   the resource `aoai-ai-support-dev`.
4. Select **Review + create**, then **Create**.
5. Open the resource and select **Model deployments** or **Deployments**.
6. Select **Create new deployment**.
7. Deploy an embedding model available in your region. Use the deployment name
   `text-embedding-model`.
8. Deploy a chat model available to your subscription. Use the deployment name
   `support-chat-model`.
9. Record the endpoint and deployment names in Azure App Settings or Key Vault.

Model names and availability change. Select the current supported model in the
Portal rather than assuming a specific model name. The application must use the
deployment names, not only the underlying model names.

## 7. Create Key Vault

1. Search for **Key vaults** and select **Create**.
2. Select `rg-ai-support-dev` and name the vault `kv-ai-support-dev-<unique>`.
3. Use the same region as the application.
4. Keep public network access restricted where possible.
5. Select **Review + create**, then **Create**.
6. Open the vault and add secrets for values such as:

```text
AZURE-OPENAI-ENDPOINT
AZURE-OPENAI-API-KEY
AZURE-SEARCH-ENDPOINT
AZURE-SEARCH-API-KEY
STORAGE-CONNECTION-STRING
```

Prefer managed identity and role-based access over keys whenever the selected
Azure SDK and service support it.

## 8. Create the Function App

1. Search for **Function App** and select **Create**.
2. Choose **Function App** with the hosting option appropriate for Python.
3. Select `rg-ai-support-dev`.
4. Enter `func-ai-support-dev-<unique>` as the app name.
5. Select **Code** as the deployment type.
6. Select **Python** and the Python version supported by the application.
7. Select Linux for the operating system.
8. Choose a development hosting plan. Use a production-capable plan when the
   application requires private networking, longer processing, or predictable
   performance.
9. Select the existing Application Insights resource when asked.
10. Select **Review + create**, then **Create**.

After creation, open **Settings > Configuration** and add the application
settings required by `src/config.py` and the Azure clients:

```text
ADMIN_EMAIL
AZURE_STORAGE_ACCOUNT_URL
AZURE_STORAGE_CONTAINER=documents
AZURE_SEARCH_ENDPOINT
AZURE_SEARCH_INDEX_NAME=support-chunks
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_CHAT_DEPLOYMENT=support-chat-model
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-model
```

Use Key Vault references or managed identity instead of putting secret values
directly in this list.

## 9. Connect Blob Storage to Event Grid

1. Open the storage account.
2. Select **Events** or **Event Grid** from the resource menu.
3. Select **+ Event Subscription**.
4. Name it `evg-ai-support-dev`.
5. Set the event type to **Blob Created**.
6. Filter the subject to the `documents` container if the Portal offers a
   subject filter.
7. Choose the Function endpoint as the destination after the ingestion
   Function exists.
8. Select **Create**.

If the Portal does not show the Function endpoint yet, create the Event Grid
subscription after deployment from the Function App's Event Grid integration
screen.

## 10. Prepare the Application for Deployment

Before deploying, confirm the repository contains:

```text
requirements.txt
host.json
src/
docs/
prompts/
```

The Python application should use Pydantic models for API requests, API
responses, settings, and data entering from Azure services. Use `@dataclass`
only for trusted internal values such as an already-validated document chunk.

The application should provide separate handlers or routes for:

- Uploading a document
- Receiving the blob-created ingestion event
- Asking a question
- Listing documents
- Viewing document status

The ingestion handler must be idempotent. If Azure retries an event, it should
not create duplicate chunks for the same document version.

## 11. Deploy Through the UI

You can deploy from VS Code using the Azure Functions extension:

1. Install the **Azure Functions** extension in VS Code.
2. Sign in to the Azure account that owns `rg-ai-support-dev`.
3. Open the `ai-support-assistant` project folder.
4. Open the Azure view and expand the subscription.
5. Expand **Function App** and locate `func-ai-support-dev-<unique>`.
6. Use the project context menu and select **Deploy to Function App**.
7. Confirm the target Function App and accept the deployment warning.
8. Wait for the deployment to finish.

Alternatively, open the Function App in the Azure Portal and use **Deployment
Center** to configure a GitHub repository and branch. Use the branch that
contains the application code and keep infrastructure documentation changes in
the same pull request only if that is your team convention.

## 12. Connect the Ingestion Function

After deployment:

1. Open the Function App in the Portal.
2. Confirm the ingestion HTTP or Event Grid-triggered Function is listed.
3. Open **Integration** for that Function.
4. Add or confirm the Event Grid trigger for the `documents` container.
5. Confirm the Function identity has access to Blob Storage, Azure AI Search,
   Azure OpenAI, and Key Vault.
6. Upload one small test document to the `documents` container.
7. Check Application Insights logs for extraction, chunking, embedding, and
   indexing messages.
8. Confirm the document status becomes `ready`.
9. Search the `support-chunks` index and verify that the source path and chunk
   content are present.

## 13. Test the Query API

1. Open the deployed Function App and select **Functions**.
2. Open the query Function and use **Get Function URL** if the endpoint is
   protected by a function key.
3. Send a question that is answered by the uploaded document.
4. Confirm the response contains an answer and source reference.
5. Send a question unrelated to the document collection.
6. Confirm the response says that there is not enough evidence instead of
   inventing an answer.
7. Check Application Insights for errors and latency.

## 14. Handle Later Document Uploads

Every upload should create a document ID and version. The processing status
should move through:

```text
uploaded -> processing -> ready
                    \-> failed
```

For a replacement document, process the new version into a temporary or
version-filtered set of search records. Activate the new version only after
all chunks are indexed successfully. Retain the old Blob file until the
retention policy says it can be deleted.

## 15. Final Checklist

- [ ] Original documents are private in Blob Storage.
- [ ] The ingestion trigger runs only for the `documents` container.
- [ ] The Search index contains chunks and matching vectors.
- [ ] The embedding deployment and Search vector dimensions match.
- [ ] The Function App can read Blob Storage.
- [ ] The Function App can write to Azure AI Search.
- [ ] Secrets are in Key Vault or managed identity, not source code.
- [ ] Application Insights receives logs.
- [ ] A supported question returns an answer with a source.
- [ ] An unsupported question returns an insufficient-evidence response.
- [ ] Reprocessing the same event does not create duplicate chunks.

DeepEval evaluation is intentionally postponed until the application and Azure
deployment are working end to end.