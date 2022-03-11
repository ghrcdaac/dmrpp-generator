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
- Release note [v3.3.0.beta](https://ghrcdaac.github.io/dmrpp-generator/#v330beta).
- Release note [v3.2.1](https://ghrcdaac.github.io/dmrpp-generator/#v321).
- Release note [v3.2.0](https://ghrcdaac.github.io/dmrpp-generator/#v320).
- Release note [v3.1.2](https://ghrcdaac.github.io/dmrpp-generator/#v312).
- Release note [v3.1.1](https://ghrcdaac.github.io/dmrpp-generator/#v311).
- Release note [v3.1.0](https://ghrcdaac.github.io/dmrpp-generator/#v310).
- Release note [v3.0.1.beta](https://ghrcdaac.github.io/dmrpp-generator/#v301beta).
- Release note [v2.1.1](https://ghrcdaac.github.io/dmrpp-generator/#v211).
- Release note [v2.1.0](https://ghrcdaac.github.io/dmrpp-generator/#v210).
- Release note [v2.0.1](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v2.0.0](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.1.0](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.0.6](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.0.5](https://ghrcdaac.github.io/dmrpp-generator/).
- Release note [v1.0.4](https://ghrcdaac.github.io/dmrpp-generator/).

## Versioning
We are following `v<major>.<minor>.<patch>` versioning convention, where:
* `<major>+1` means we changed the infrastructure and/or the major components that makes this software run. Will definitely
  lead to breaking changes.
* `<minor>+1` means we upgraded/patched the dependencies this software relays on. Can lead to breaking changes.
* `<patch>+1` means we fixed a bug and/or added a feature. Breaking changes are not expected.

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
  region = var.region
  prefix = var.prefix
  docker_image = var.dmrpp-generator-docker-image

  // Optional parameters
  cpu = 800 // default to 800
  enable_cw_logging = False // default to False
  memory_reservation = 900 // default to 900
  prefix = "Cumulus stack prefix" // default Cumulus stack prefix
  desired_count = 1  // Default to 1
  log_destination_arn = var.aws_log_mechanism // default to null
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

## Cumulus Collection Configuration

Add the options desired to the collection definition as follows:

```code
{
  "config": {
    "meta": {
      "dmrpp": {
        "options": [
          {
            "flag": "-M"
          },
          {
            "flag": "-s",
            "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config",
            "download": "true"
          },
          {
            "flag": "-c",
            "opt": "s3://ghrcsbxw-public/aces1cont__1/aces1cont_2002.212_v2.50.tar.cmr.json",
            "download": "false"
          }
        ]
      }
    }
  }
}
```

For a list of all configuration options see: https://docs.opendap.org/index.php?title=DMR%2B%2B#:~:text=4.2%20Command%20line%20options


## Cumulus Workflow Configuration

If your workflow is used by multiple collections which use a common dmrpp
config, the config can be set at the workflow's
`${StepName}.Parameters.cma.task_config.dmrpp` instead of in the collection
(**Note:** if the workflow and collection _both_ have a `dmrpp` key, the
collection's config will be used; the workflow's `dmrpp` acts as the default
which can be overridden by any collection that needs a different config):

```
# terraform

dmrpp_config = {
  options = [
    {
      flag = "-M"
    },
    {
      flag = "-s"
      opt = "s3://ghrcsbxw-public/dmrpp_config/file.config"
      download = "true"
    },
    {
      flag = "-c"
      opt = "s3://ghrcsbxw-public/aces1cont__1/aces1cont_2002.212_v2.50.tar.cmr.json"
      download = "false"
    }
  ]
}

# workflow JSON
   "HyraxProcessing": {
      "Parameters": {
        "cma": {
          "event.$": "$",
          "task_config": {
            ...
            "dmrpp": ${jsonencode(dmrpp_config)}
          }
        }
      },

    ...
    }
```
