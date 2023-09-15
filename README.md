```code
 ____  __  __ ____  ____  ____
|  _ \|  \/  |  _ \|  _ \|  _ \
| | | | |\/| | |_) | |_) | |_) |
| |_| | |  | |  _ <|  __/|  __/
|____/|_|  |_|_| \_\_|   |_|
```

# Overview
This repo consists of two components. The DMR++ activity terraform module and a python CLI to the DMR++ Docker 
container.

Current OPeNDAP BESD image:
https://github.com/ghrcdaac/dmrpp-generator/blob/ce1b53772cf9d501d4576a8d94f4f6868e526f7d/Dockerfile#L1

## Versioning
We are following `v<major>.<minor>.<patch>` versioning convention, where:
* `<major>+1` means we changed the infrastructure and/or the major components that makes this software run. Will definitely
  lead to breaking changes.
* `<minor>+1` means we upgraded/patched the dependencies this software relays on. Can lead to breaking changes.
* `<patch>+1` means we fixed a bug and/or added a feature. Breaking changes are not expected.

# Pre-requisite
The prerequisites depend on which use case is needed. 

## Terraform Module
This module is meant to used within the Cumulus stack.
If you don't have Cumulus stack deployed yet please consult [this repo](https://github.com/nasa/cumulus)
and follow the [documetation](https://nasa.github.io/cumulus/docs/cumulus-docs-readme) to provision it.

## DMR++ Python CLI
For each release after v4.1.0, there will be a python wheel published in the release assets. This can be installed and 
used locally via pip like the following:
`pip install https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.0-test/dmrpp_file_generator-4.1.2-py3-none-any.whl`
The python module uses Docker compose to generate dmrpp files locally so no other dependencies should be needed.

# Deploying the Terraform module with the Cumulus Stack
In [main.tf](https://github.com/nasa/cumulus-template-deploy/blob/master/cumulus-tf/main.tf) file
 (where you defined cumulus module) add
 ```terraform
module "dmrpp-generator" {
  // Required parameters
  source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/<tag_num>/dmrpp-generator.zip"
  cluster_arn = module.cumulus.ecs_cluster_arn
  region = var.region
  prefix = var.prefix
  

  // Optional parameters
  docker_image = "ghrcdaac/dmrpp-generator:<tag_num>" // default to the correct release
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
configurations will be merged together, with the collection's config overriding
any keys that are found in both the workflow and collection):

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

## Timeout Configuration
The subprocess call to the BESD library has a configurable timeout value. It will default to 60 seconds
if not configured. There are two ways to provide a custom value. 
1. Setting the `get_dmrpp_timeout` terraform variable
2. Adding `get_dmrpp_timeout` to the collection definition: `collection.meta.dmrpp`

If the value is provided in the collection definition this will take precedence over the environment
variable.

## Subprocess Logging Configuration
When making the subprocess call, stdout and stderr will default to `None` to prevent an issue from occurring where the 
timeout is not respected. This can be configured in two ways.
1. Setting the `ENABLE_SUBPROCESS_LOGGING` environment variable in terraform
2. Adding `enable_subprocess_logging` to the collection definition: `collection.meta.dmrpp`. Can be `true` or `false`.

If the value is provided in the collection definition this will take precedence over the environment
variable.

# DMR++ Python CLI
# How to install
Find the version you want to use and get the asset URL for the .whl file and install like the following example command:
```shell
pip install https://github.com/ghrcdaac/dmrpp-generator/releases/download/v<release_version>/dmrpp_file_generator-<dmrpp_version>-py3-none-any.whl
```

# Supported get_dmrpp configuration
## Via env vars
Create a PAYLOAD environment variable holding dmrpp options
```
PAYLOAD='{"dmrpp_regex": "^.*.nc4", "options":[{"flag": "-M"}, {"flag": "-s", "opt": "s3://ghrcsbxw-public/dmrpp_config/file.config","download": "true"}]}'
```
`dmrpp_regex` is optional to override the DMRPP-Generator regex

# Generate DMRpp files locally without Hyrax server
`dmrpp` now uses docker compose v2.  Please update to  
docker compose v2 or you will get the error  
`/bin/sh: 1: docker compose: not found`

Overview:
```shell
$ dmrpp -h
usage: dmrpp [-h] -p NC_HDF_PATH [-prt PORT] [-pyld PAYLOAD] [--validate] [--no-validate]

Generate and validate DMRPP files. Any DMR++ commandline option can be provided in addition to the options listed below. To see what options are available check the documentation:
https://docs.opendap.org/index.php?title=DMR%2B%2B#Command_line_options

optional arguments:
  -h, --help            show this help message and exit
  -p NC_HDF_PATH, --path NC_HDF_PATH
                        Path to netCDF4 and HDF5 folder
  -prt PORT, --port PORT
                        Port number to Hyrax local server
  -pyld PAYLOAD, --payload PAYLOAD
                        Payload to pass to the besd get_dmrpp call. If not set, will check for PAYLOAD environment variable, or default to '{}'
  --validate            Validate netCDF4 and HDF5 files against OPeNDAP local server. This is the default behavior
  --no-validate         Do not validate netCDF4 and HDF5 files against OPeNDAP local server. The default behavior is --validate.


```

The folder `<absolute/path/to/files>` should contain netCDF and/or HDF files
```shell
$ dmrpp --path /home/michael/dmrpp-generator/temp/ --no-validate
```

# Generate DMRpp files locally with Hyrax server (for validation)
```shell
$ dmrpp --path /home/michael/dmrpp-generator/temp/ --validate
Log file: /tmp/dmrpp-generator-13z6cizs
Results served at : http://localhost:8080/opendap (^C to kill the server)
^C
Shutting down the server...
```
A prompt will ask you to visit localhost:8080. If you want to change the default port run the command with
```shell
$ dmrpp --path /home/michael/dmrpp-generator/temp/ --validate -prt 8889
Log file: /tmp/dmrpp-generator-34blq6gn
Results served at : http://localhost:8889/opendap (^C to kill the server)
^C
Shutting down the server...
```
