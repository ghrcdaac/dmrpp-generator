
# 📖 Release notes

## v1.1.0
This release:
* Fixes the file type issue, now you can define a custom dmrpp file type.
* Uses a new hyrax release [base_image](https://hub.docker.com/r/opendap/besd)

## v1.0.6
This release:
* Fixes the issue of AWS provider [issue#10](https://github.com/ghrcdaac/dmrpp-generator/issues/10)
* Reads from `url_path` key passed in the payload. Also, the provider was taking off from the main.tf

## v1.0.5
This release fixes the problem adding a type of meta data for the dmrpp file and also changing some spacings.

## v1.0.4
This release fixes the problem of assuming the granuleId is the same as the file name [issue#9](https://github.com/ghrcdaac/dmrpp-generator/issues/9)


## 🏃 Migration Steps to v1.1.0
Change the source url in your terraform file to point to v1.1.0 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.1.0/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.1.0 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.1.0"
}

```

## 🏃 Migration Steps to v1.0.6
Change the source url in your terraform file to point to v1.0.6 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.6/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.6 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.6"
}

```

## 🏃 Migration Steps to v1.0.5
Change the source url in your terraform file to point to v1.0.5 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.5/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.5 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.5"
}

```

## 🏃 Migration Steps to v1.0.4
Change the source url in your terraform file to point to v1.0.4 release
```code
module "dmrpp-generator" {
source = "https://github.com/ghrcdaac/dmrpp-generator/releases/download/v1.0.4/dmrpp-generator.zip"
...
}
``` 
Change the value of your docker image to point to v1.0.4 tag
```code
module "dmrpp-generator" {
...
docker_image = "ghrcdaac/dmrpp-generator:v1.0.4"
}

```
## 🚨 Breaking Changes
The workflow is accepting the whole payload 
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
