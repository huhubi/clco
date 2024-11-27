

#  Infrastructure-as-Code: Getting to know Pulumi

Starting point for building web application hosted in Azure App Service.

Solution description for the follwing assingment (see monograph.pdf for more details):

"Pulumi allows you to define infrastructure using familiar programming languages, making your
infrastructure scripts reusable and version-controlled. In this assignment, you will develop a
Pulumi script to provision an Azure resource group and a storage account within it."
## How To Setup Pulumi
1. Create a new project(only if folder hasnt been creeated yet):
    ```bash
    $ pulumi new azuretest
    ```
1. Create a new stack:

    ```bash
    $ pulumi stack init dev
    ```

1. Login to Azure CLI (you will be prompted to do this during deployment if you forget this step):

    ```bash
    $ az login
    ```


1. Specify the Azure location to use:

    ```bash
    $ pulumi config set azure-native:location northeurope
    ```

1. Define Storage Account Name:

    ```bash
    $ pulumi config set azure-resources:storageAccountName mystorageaccount123huma
    ```

1. Specify SKU for the Storage Account:

    ``` bash
    $ pulumi config set azure-resources:skuName Standard_LRS
    ```

1. Set Ressource group name:

   ```bash
   $ pulumi config set azure-resources:resourceGroupName myResourceGroup123huma
   ```
1. pulumi up (-y to skip confirmation):

    ```bash
   $ pulumi up -y
         Previewing update (dev)
 
             Type                                     Name                 Plan
         +   pulumi:pulumi:Stack                      azure-resources-dev  create
         +   ├─ azure-native:resources:ResourceGroup  resourceGroup        create                                                                                                                                                           
         +   └─ azure-native:storage:StorageAccount   storageAccount       create                                                                                                                                                           
         Resources:
         + 3 to create
   
         Updating (dev)
   
         Type                                     Name                 Status
         +   pulumi:pulumi:Stack                      azure-resources-dev  created (39s)
         +   ├─ azure-native:resources:ResourceGroup  resourceGroup        created (6s)
         +   └─ azure-native:storage:StorageAccount   storageAccount       created (21s)
         Resources:
         + 3 created

         Duration: 40s
        ```
   
## Cleanup pulumi

1. Destroy stack(-y to skip confirmation) :
   ```bash
    $ pulumi destroy -y
   Previewing destroy (dev)


     Type                                     Name                 Plan                                                                                                                                                             
   -   pulumi:pulumi:Stack                      azure-resources-dev  delete                                                                                                                                                           
   -   ├─ azure-native:storage:StorageAccount   storageAccount       delete                                                                                                                                                           
   -   └─ azure-native:resources:ResourceGroup  resourceGroup        delete                                                                                                                                                           
   Resources:
   - 3 to delete

   Destroying (dev)

     Type                                     Name                 Status
    -   pulumi:pulumi:Stack                      azure-resources-dev  deleted (0.93s)
    -   ├─ azure-native:storage:StorageAccount   storageAccount       deleted (12s)
    -   └─ azure-native:resources:ResourceGroup  resourceGroup        deleted (17s)
    Resources:
    - 3 deleted

   Duration: 34s
    ```

1. If pulumi is messed up:
   ```bash
    $ pulumi cancel
    ```

1. Delte pulumi stack after excercise:
   ```bash
    $ pulumi stack rm dev
    ```
