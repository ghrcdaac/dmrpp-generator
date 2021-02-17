```code
 ____  __  __ ____  ____  ____
|  _ \|  \/  |  _ \|  _ \|  _ \
| | | | |\/| | |_) | |_) | |_) |
| |_| | |  | |  _ <|  __/|  __/
|____/|_|  |_|_| \_\_|   |_|
```


# Overview
DMR++ files generator is a cloud based activity that generate DMRPP files from netCDF4 and HDF files
## 📖 Documentation
- Release note [v1.0.6](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.0.5](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.0.4](https://ghrcdaac.github.io/dmrpp-generator/).

# 🔨 Pre-requisite 
This module is meant to run within Cumulus stack. 
If you don't have Cumulus stack deployed yet please consult [this repo](https://github.com/nasa/cumulus) 
and follow the [documetation](https://nasa.github.io/cumulus/docs/cumulus-docs-readme) to provision it.

# Deploying with Cumulus Stack
In [main.tf](https://github.com/nasa/cumulus-template-deploy/blob/master/cumulus-tf/main.tf) file
 (where you defined cumulus module) add 
 ```code
module "dmrpp-generator" {
  // Required parameters
  source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/<tag_num>/dmrpp-generator.zip"
  cluster_arn = module.cumulus.ecs_cluster_arn
  log2elasticsearch_lambda_function_arn = module.cumulus.log2elasticsearch_lambda_function_arn
  region = var.region
  prefix = var.prefix
  docker_image = var.dmrpp-generator-docker-image

  // Optional parameters
  cpu = 800 // default to 800
  memory_reservation = 900 // default to 900
  prefix = "Cumulus stack prefix" // default Cumulus stack prefix
  desired_count = 1  // Default to 1
  docker_image = "ghrcdaac/dmrpp-generator:<tag_num>"
} 
```
In [variables.tf](https://github.com/nasa/cumulus-template-deploy/blob/master/cumulus-tf/variables.tf) 
file you need to define 
```code
variable "dmrpp-generator-docker-image" {
  default = "ghrcdaac/dmrpp-generator:<tag_num>"
}
```
Assuming you already defined the region and the prefix 


# Add the activity to your workflow
In your [workflow.tf](https://github.com/nasa/cumulus-template-deploy/blob/master/cumulus-tf/hello_world_workflow.tf) add 
```code
   "HyraxProcessing": {
      "Parameters": {
        "cma": {
          "event.$": "$",
          "task_config": {
            "buckets": "{$.meta.buckets}",
            "distribution_endpoint": "{$.meta.distribution_endpoint}",
            "files_config": "{$.meta.collection.files}",
            "fileStagingDir": "{$.meta.collection.url_path}",
            "granuleIdExtraction": "{$.meta.collection.granuleIdExtraction}",
            "collection": "{$.meta.collection}"
          }
        }
      },
      "Type": "Task",
      "Resource": "${module.dmrpp-generator.dmrpp_task_id}",
      "Catch": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "ResultPath": "$.exception",
          "Next": "WorkflowFailed"
        }
      ],
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 2,
          "MaxAttempts": 3
        }
      ],
      "Next": "<Your next Step>"
    }
```
Where `<Your next Step>` is the next step in your workflow.
