---
layout: Conceptual
monikers:
- azureml-api-2
defaultMoniker: azureml-api-2
versioningType: Ranged
title: 'Tutorial: Upload, access, and explore your data - Azure Machine Learning | Microsoft Learn'
canonicalUrl: https://learn.microsoft.com/en-us/azure/machine-learning/tutorial-explore-data?view=azureml-api-2
config_moniker_range: azureml-api-2 || azureml-api-1
breadcrumb_path: ../breadcrumb/azure-ai/toc.json
feedback_help_link_url: https://learn.microsoft.com/answers/tags/75/azure-machine-learning/
feedback_help_link_type: get-help-at-qna
feedback_product_url: https://feedback.azure.com/d365community/forum/b9a0c624-ad25-ec11-b6e6-000d3a4f09d0
feedback_system: Standard
permissioned-type: public
recommendations: true
recommendation_types:
- Training
- Certification
uhfHeaderId: azure-ai-foundry
ms.suite: office
learn_banner_products:
- azure
manager: 'mcleans '
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 365-days
description: Upload data to cloud storage, create an Azure Machine Learning data asset, create new versions for data assets, and use the data for interactive development.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
ms.reviewer: metang
author: johnwu0604
ms.author: wujohn
ms.date: 2026-08-21T00:00:00.0000000Z
ai-usage: ai-assisted
locale: en-us
document_id: d1d58dd4-b06b-ac11-7afc-06ec4413296b
document_version_independent_id: 13d30b62-3001-0faf-528b-247cfa2e89ac
updated_at: 2026-10-19T22:12:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/azure-ai-docs-pr/blob/live/articles/machine-learning/tutorial-explore-data.md
gitcommit: https://github.com/MicrosoftDocs/azure-ai-docs-pr/blob/a6bffc1f0d8ff3419117a74ac3db4b3ef869e440/articles/machine-learning/tutorial-explore-data.md
git_commit_id: a6bffc1f0d8ff3419117a74ac3db4b3ef869e440
default_moniker: azureml-api-2
site_name: Docs
depot_name: Learn.azure-ai
page_type: conceptual
toc_rel: toc.json
word_count: 2298
asset_id: machine-learning/tutorial-explore-data
moniker_range_name: 98205f26d9f91dafa7599e4683fa1e61
monikers:
- azureml-api-2
item_type: Content
source_path: articles/machine-learning/tutorial-explore-data.md
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/d6f38669-3d05-40f2-afd8-e49f7dd20884
- https://authoring-docs-microsoft.poolparty.biz/devrel/fcc3cd4a-59ea-47a2-9cc1-784142a5a25d
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/55265cca-de9b-48dc-a77a-9047cc39a575
- https://authoring-docs-microsoft.poolparty.biz/devrel/d7a55faf-a992-4e27-aa3a-eadc9830e778
platformId: 006fd8a8-bae5-c10e-75a8-97fc0ec186b9
---

# Tutorial: Upload, access, and explore your data - Azure Machine Learning | Microsoft Learn

**APPLIES TO**: ![](media/yes.png)[Python SDK azure-ai-ml **v2 (current)**](https://aka.ms/sdk-v2-install)

In this tutorial, you use an Azure Machine Learning notebook to upload a sample dataset, register it as a versioned data asset, and access it with Python for interactive exploration. Specifically, you:

- Upload your data to cloud storage
- Create an Azure Machine Learning data asset
- Access your data in a notebook for interactive development
- Create new versions of data assets

A machine learning project typically starts with exploratory data analysis (EDA), data preprocessing (cleaning, feature engineering), and building machine learning model prototypes to validate hypotheses. This *prototyping* project phase is highly interactive and lends itself to development in an IDE or a Jupyter notebook with a *Python interactive console*. This tutorial describes these concepts.

## Prerequisites

1. To use Azure Machine Learning, you need a workspace. If you don't have one, complete [Create resources you need to get started](quickstart-create-resources) to create a workspace and learn more about using it.

    Important

    If your Azure Machine Learning workspace is configured with a managed virtual network, you might need to add outbound rules to allow access to the public Python package repositories. For more information, see [Scenario: Access public machine learning packages](/en-us/azure/machine-learning/how-to-managed-network#scenario-access-public-machine-learning-packages).
2. Sign in to the [studio](https://ml.azure.com) and select your workspace if it's not already open.
3. Open or create a notebook in your workspace:

    - If you want to copy and paste code into cells, create [a new notebook](quickstart-create-resources#create-a-new-notebook).
    - Or, open **tutorials/get-started-notebooks/explore-data.ipynb** from the **Samples** section of studio. Then select **Clone** to add the notebook to your **Files**. To find sample notebooks, see [Learn from sample notebooks](quickstart-create-resources#learn-from-sample-notebooks).

## Set your kernel and open in Visual Studio Code (VS Code)

1. On the top bar above your opened notebook, create a compute instance if you don't already have one.

    [![Screenshot shows how to create a compute instance.](media/tutorial-azure-ml-in-a-day/create-compute.png)](media/tutorial-azure-ml-in-a-day/create-compute.png#lightbox)
2. If the compute instance is stopped, select **Start compute** and wait until it's running.

    [![Screenshot shows how to start a stopped compute instance.](media/tutorial-azure-ml-in-a-day/start-compute.png)](media/tutorial-azure-ml-in-a-day/start-compute.png#lightbox)
3. Wait until the compute instance is running. Then make sure that the kernel, found on the top right, is `Python 3.10 - SDK v2`. If not, use the dropdown list to select this kernel.

    [![Screenshot shows how to set the kernel.](media/tutorial-azure-ml-in-a-day/set-kernel.png)](media/tutorial-azure-ml-in-a-day/set-kernel.png#lightbox)

    If you don't see this kernel, verify that your compute instance is running. If it is, select the **Refresh** button on the top right of the notebook.
4. If you see a banner that says you need to be authenticated, select **Authenticate**.
5. You can run the notebook here, or open it in VS Code for a full integrated development environment (IDE) with the power of Azure Machine Learning resources. Select **Open in VS Code**, then select either the web or desktop option. When launched this way, VS Code is attached to your compute instance, the kernel, and the workspace file system.

    [![Screenshot shows how to open the notebook in VS Code.](media/tutorial-azure-ml-in-a-day/open-vs-code.png)](media/tutorial-azure-ml-in-a-day/open-vs-code.png#lightbox)

Important

The rest of this tutorial contains cells of the tutorial notebook. Copy and paste them into your new notebook, or switch to the notebook now if you cloned it.

## Download the data used in this tutorial

This tutorial uses a CSV-format credit card client data sample. The steps take place in an Azure Machine Learning resource. In that resource, you create a local folder with the suggested name of **data**, directly under the folder where this notebook is located.

Note

This tutorial depends on data placed in an Azure Machine Learning resource folder location. For this tutorial, 'local' means a folder location in that Azure Machine Learning resource.

1. Select **Open terminal** below the three dots, as shown in this image:

    ![Screenshot shows open terminal tool in notebook toolbar.](media/tutorial-cloud-workstation/open-terminal.png)
2. The terminal window opens in a new tab.
3. Make sure you change directory (`cd`) to the same folder where this notebook is located. For example, if the notebook is in a folder named **get-started-notebooks**:

    ```bash
    cd get-started-notebooks    # modify this to the path where your notebook is located
    ```
4. Enter these commands in the terminal window to copy the data to your compute instance:

    ```bash
    mkdir data
    cd data                     # the subfolder where you'll store the data
    wget https://azuremlexamples.blob.core.windows.net/datasets/credit_card/default_of_credit_card_clients.csv
    ```
5. You can now close the terminal window.

For more information about the data in the UC Irvine Machine Learning Repository, visit [this resource](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients).

## Create a handle to the workspace

Before you explore the code, you need a way to reference your workspace. You create `ml_client` as a handle to the workspace. You then use `ml_client` to manage resources and jobs.

In the next cell, enter your Subscription ID, Resource Group name, and Workspace name. To find these values:

1. In the upper right Azure Machine Learning studio toolbar, select your workspace name.
2. Copy the value for workspace, resource group, and subscription ID into the code.
3. You must copy each value individually, one at a time. Close the area, paste the value, then continue to the next one.

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# authenticate
try:
    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")
except Exception:
    credential = InteractiveBrowserCredential()

# Get a handle to the workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="<SUBSCRIPTION_ID>",
    resource_group_name="<RESOURCE_GROUP>",
    workspace_name="<AML_WORKSPACE_NAME>",
)
```

Note

Creating MLClient won't connect to the workspace. The client initialization is lazy and waits for the first time it needs to make a call. This happens in the next code cell.

## Upload data to cloud storage

Azure Machine Learning uses Uniform Resource Identifiers (URIs), which point to storage locations in the cloud. A URI makes it easy to access data in notebooks and jobs. Data URI formats are similar to the web URLs that you use in your web browser to access web pages. For example:

- Access data from public https server: `https://<account_name>.blob.core.windows.net/<container_name>/<folder>/<file>`
- Access data from Azure Data Lake Gen 2: `abfss://<file_system>@<account_name>.dfs.core.windows.net/<folder>/<file>`

An Azure Machine Learning data asset is similar to web browser bookmarks (favorites). Instead of remembering long storage paths (URIs) that point to your most frequently used data, you can create a data asset and then access that asset with a friendly name.

Data asset creation also creates a *reference* to the data source location, along with a copy of its metadata. When the data already resides in cloud storage, it stays in place, so you incur no extra storage cost and don't risk data source integrity. When you create a data asset from local files, as in this tutorial, Azure Machine Learning uploads them to the workspace's default datastore, which can incur storage costs. You can create data assets from Azure Machine Learning datastores, Azure Storage, public URLs, and local files.

Tip

For smaller data uploads, Azure Machine Learning data asset creation works well for uploading data from local machine resources to cloud storage. This approach avoids the need for extra tools or utilities. However, larger data uploads might require a dedicated tool or utility - for example, **azcopy**. The azcopy command-line tool moves data to and from Azure Storage. For more information about azcopy, see [Get started with AzCopy](/en-us/azure/storage/common/storage-use-azcopy-v10).

The next notebook cell creates the data asset. The code sample uploads the raw data file to the designated cloud storage resource.

Each time you create a data asset, you need a unique version for it. If the version already exists, you get an error. In this code, you use "initial" for the first read of the data. If that version already exists, the code doesn't recreate it.

You can also omit the **version** parameter. In this case, a version number is generated for you, starting with 1 and incrementing from there.

This tutorial uses the name "initial" as the first version. The [Create production machine learning pipelines](tutorial-pipeline-python-sdk) tutorial also uses this version of the data, so you use a value that you see again in that tutorial.

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# Update the 'my_path' variable to match the location of where you downloaded the data on your
# local filesystem

my_path = "./data/default_of_credit_card_clients.csv"
# Set the version number of the data asset
v1 = "initial"

my_data = Data(
    name="credit-card",
    version=v1,
    description="Credit card data",
    path=my_path,
    type=AssetTypes.URI_FILE,
)

## Create data asset if it doesn't already exist:
try:
    data_asset = ml_client.data.get(name="credit-card", version=v1)
    print(
        f"Data asset already exists. Name: {my_data.name}, version: {my_data.version}"
    )
except:
    ml_client.data.create_or_update(my_data)
    print(f"Data asset created. Name: {my_data.name}, version: {my_data.version}")
```

To examine the uploaded data, select **Data** in the **Assets** section of the left-hand navigation menu. The data is uploaded and a data asset is created:

![Screenshot shows the data in studio.](media/tutorial-explore-data/access-and-explore-data.png)

This data is named **credit-card**. In the **Data assets** tab, you can see it in the **Name** column.

An Azure Machine Learning datastore is a *reference* to an *existing* storage account on Azure. A datastore offers these benefits:

1. A common and easy-to-use API to interact with different storage types:

    - Azure Data Lake Storage
    - Blob
    - Files

    and authentication methods.
2. An easier way to discover useful datastores when working as a team.
3. In your scripts, a way to hide connection information for credential-based data access (service principal/SAS/key).

## Access your data in a notebook

You want to create data assets for frequently accessed data. You can access the data using the URI as described in [Access data from a datastore URI as you would from a filesystem](how-to-access-data-interactive#access-data-from-a-datastore-uri-as-you-would-from-a-filesystem). However, as mentioned previously, it can become difficult to remember these URIs.

An alternative is to use the `azureml-fsspec` library, which provides a file system interface for Azure Machine Learning datastores. This is an easier way to access the CSV file in Pandas:

Important

In a notebook cell, execute this code to install the `azureml-fsspec` Python library in your Jupyter kernel:

```python
%pip install -U azureml-fsspec
```

```python
import pandas as pd

# Get a handle of the data asset and print the URI
data_asset = ml_client.data.get(name="credit-card", version=v1)
print(f"Data asset URI: {data_asset.path}")

# Read into pandas - note that you will see 2 headers in your data frame - that is ok, for now

df = pd.read_csv(data_asset.path)
df.head()
```

For more information about data access in a notebook, see [Access data from Azure cloud storage during interactive development](how-to-access-data-interactive).

## Create a new version of the data asset

The data needs some light cleaning to make it suitable for training a machine learning model. It has:

- Two headers
- A client ID column that wouldn't be used as a feature in machine learning
- Spaces in the response variable name

Also, compared to the CSV format, the Parquet file format is a better way to store this data. Parquet offers compression and maintains schema. To clean the data and store it in Parquet format:

```python
# Read in data again, this time using the 2nd row as the header
df = pd.read_csv(data_asset.path, header=1)
# Rename column
df.rename(columns={"default payment next month": "default"}, inplace=True)
# Remove ID column
df.drop("ID", axis=1, inplace=True)

# Write file to filesystem
df.to_parquet("./data/cleaned-credit-card.parquet")
```

This table shows the structure of the data in the original **default\_of\_credit\_card\_clients.csv** file downloaded in an earlier step. The uploaded data contains 23 explanatory variables and 1 response variable, as shown here:

| Column Name(s) | Variable Type | Description |
| --- | --- | --- |
| X1 | Explanatory | Amount of the given credit (NT dollar): it includes both the individual consumer credit and their family (supplementary) credit. |
| X2 | Explanatory | Gender (1 = male; 2 = female). |
| X3 | Explanatory | Education (1 = graduate school; 2 = university; 3 = high school; 4 = others). |
| X4 | Explanatory | Marital status (1 = married; 2 = single; 3 = others). |
| X5 | Explanatory | Age (years). |
| X6-X11 | Explanatory | History of past payment. Past monthly payment records tracked from April to September 2005. -1 = pay duly; 1 = payment delay for one month; 2 = payment delay for two months; . . .; 8 = payment delay for eight months; 9 = payment delay for nine months and above. |
| X12-17 | Explanatory | Amount of bill statement (NT dollar) from April to September 2005. |
| X18-23 | Explanatory | Amount of previous payment (NT dollar) from April to September 2005. |
| Y | Response | Default payment (Yes = 1, No = 0) |

Next, create a new *version* of the data asset. The data automatically uploads to cloud storage. For this version, add a time value so that each time this code runs, a different version number is created.

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
import time

# Next, create a new version of the data asset (the data is automatically uploaded to cloud storage):
v2 = "cleaned" + time.strftime("%Y.%m.%d.%H%M%S", time.gmtime())
my_path = "./data/cleaned-credit-card.parquet"

# Define the data asset, and use tags to make it clear the asset can be used in training

my_data = Data(
    name="credit-card",
    version=v2,
    description="Default of credit card clients data.",
    tags={"training_data": "true", "format": "parquet"},
    path=my_path,
    type=AssetTypes.URI_FILE,
)

## Create the data asset

my_data = ml_client.data.create_or_update(my_data)

print(f"Data asset created. Name: {my_data.name}, version: {my_data.version}")
```

The cleaned Parquet file is the latest version data source. This code shows the CSV version result set first, then the Parquet version:

```python
import pandas as pd

# Get a handle of the data asset and print the URI
data_asset_v1 = ml_client.data.get(name="credit-card", version=v1)
data_asset_v2 = ml_client.data.get(name="credit-card", version=v2)

# Print the v1 data
print(f"V1 Data asset URI: {data_asset_v1.path}")
v1df = pd.read_csv(data_asset_v1.path)
print(v1df.head(5))

# Print the v2 data
print(
    "_____________________________________________________________________________________________________________\n"
)
print(f"V2 Data asset URI: {data_asset_v2.path}")
v2df = pd.read_parquet(data_asset_v2.path)
print(v2df.head(5))
```

## Clean up resources

If you plan to continue now to other tutorials, skip to Next steps.

### Stop compute instance

If you don't plan to use it now, stop the compute instance:

1. In the studio, in the left pane, select **Compute**.
2. In the top tabs, select **Compute instances.**
3. Select the compute instance in the list.
4. On the top toolbar, select **Stop**.

### Delete all resources

Important

The resources that you created can be used as prerequisites to other Azure Machine Learning tutorials and how-to articles.

If you don't plan to use any of the resources that you created, delete them so you don't incur any charges:

1. In the Azure portal, in the search box, enter *Resource groups* and select it from the results.
2. From the list, select the resource group that you created.
3. In the **Overview** page, select **Delete resource group**.

    ![Screenshot of the selections to delete a resource group in the Azure portal.](includes/media/aml-delete-resource-group/delete-resources.png)
4. Enter the resource group name. Then select **Delete**.