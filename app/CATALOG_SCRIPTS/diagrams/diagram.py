from diagrams import Cluster, Diagram

from diagrams.onprem.client import User
from diagrams.onprem.container import Docker

from diagrams.programming.framework import Flask
from diagrams.programming.language import Java

from diagrams.onprem.client import Users
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.compute import VM

with Diagram("Automated detailed lineage service for EDC", show=False):
    source = Users("Data owners")

    with Cluster("Event Flows"):
        with Cluster("Uploading Excel"):
            workers = [StorageAccounts("Container_1"),
                       StorageAccounts("Container_2"),
                       StorageAccounts("Container_3")]

        with Cluster("Transform & upload data"):
            python = Flask("Read & transform Excel")
                        
            container = Docker("Docker container")

        edc_app = Java("EDC application")
    
    user = User("EDC user")

    source >> workers
    workers >> python
    python >> edc_app
    edc_app >> user

    

