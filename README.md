# Infrastructure as Code (IaC)

## Abstract

This documentation weights *Hashicorp*'s [Terraform](#link-terraform) against *Google Cloud Platform*'s [Cloud Deployment Manager](#cloud-deployment-manager) and *Amazon Web Service*'s [CloudFormation](#cloudformation), providing *cons* and *pros* between them.

The goal is to shed some insight on which tool to choose for the <u>right job</u> and ultimately provide <u>guidelines and best practices</u> for each.

*Infrastructure as Code* is an easy way to declare how we want our infrastructure to look like and keep this changes versioned.

> This doesn't mean that appling the configuration will actually provision everything as we wanted.

## Table of contents

- [What is Hashicorp Terraform](#what-is-hashicorp-terraform)
  - [How Terraform works](#How-terraform-works)
  - [The Terraform state](#the-terraform-state)
  - [The Terraform lock](#the-terraform-lock)
  - [Terraform as a team](#terraform-as-a-team)
- [What is GCP Cloud Deployment Manager](#what-is-gcp-cloud-deployment-manager)
  - [How Deployment Manager works](#How-deployment-manager-works)
  - [Deployment Manager as a team](#deployment-manager-as-a-team)
- [What is AWS CloudFormation](#what-is-aws-cloudformation)
  - [How CloudFormation works](#How-cloudformation-works)
  - [CloudFormation as a team](#cloudformation-as-a-team)

## What is Hashicorp Terraform

> "[Terraform](#link-terraform) is a tool for building, changing, and versioning infrastructure safely and efficiently. [Terraform](#link-terraform) can manage existing and popular service providers as well as custom in-house solutions."

This means that we can use the `HCL` (**H**ashicorp **C**onfiguration **L**anguage) independent of the provider and provision the infrastructure following the same language.

The only differences are strictly to how that provider works in terms of resources and what type of parameters those resources accept.

The most simple usage is creating a provider and a vpc resources. This is a side by side comparison.

```terraform
provider "google" {}                              provider "aws" {
                                                    region  = var.gcp-region
                                                    profile = var.gcp-profile
                                                  }

resource "google_compute_network" "my_vpc" {      resource "aws_vpc" "my_vpc" {
  name                    = "my_vpc-tf"             cidr_block = "10.0.0.0/16"
  auto_create_subnetworks = false                   tags = {
}                                                     Name = "my_vpc-tf"
                                                    }
                                                  }
```

As seen, the resources needed and parameters of those same resources only depend on the provider specifications.

The developer experience (DX) of what will be created/updated/deleted will be pretty much identical.

> Using Terraform does not remove the need to understand how each provider works.

### Terraform state

How does Terraform stores and keeps up with the changes that will be apllied? As we seen from GCP and AWS, you get that management state either in the Cloud Development Manager or CloudFormation console / CLI / API.

With Terraform, there is the concept of backend. A configurable property that can be set to a local file, or a remote file, such as `s3` or `gcs`, among others.

This state is not a layer on top of the GCP Cloud Development Manager not of the AWS CloudFormation.

### Terraform lock

When an `apply` / `delete` action is triggered it attempts to lock the state so it can safely update it without another team member or a CD Pipeline step writes at the same time.

When this action is complete, it unlocks the state.

> When a lock is in place and another `apply` / `delete` action is triggered, it will fail and will not be queued.

## What is GCP Cloud Deployment Manager

> "A declarative approach allows the user to specify what the configuration should be and let the system figure out the steps to take."

Configure the gcloud CLI.

```bash
gcloud config set core/project my-project-id
gcloud config set compute/region my-region
gcloud config set compute/zone my-zone

gcloud config list
```

Which should output something close to:

```text
[compute]
region = my-region
zone = my-zone
[core]
account = my-email-account
disable_usage_reporting = True
project = my-project-id

Your active configuration is: [default]
```

| solution | type | language |
|---:|:---:|:---|
| Terraform | declarative | `HCL` / `JSON`
| Cloud Deployment Manager | declarative | `YAML` / `JSON`

```sh
# create deployment preview
gcloud deployment-manager deployments create deployment-demo-1 --config gcp/demo-01.yaml --preview

# update deployment preview
gcloud deployment-manager deployments update deployment-demo-1 --config gcp/demo-01.yaml --preview

# cancel a deployment preview
gcloud deployment-manager deployments cancel-preview deployment-demo-1

# update deployment
gcloud deployment-manager deployments update deployment-demo-1 --config gcp/demo-01.yaml

# delete deployment
gcloud deployment-manager deployments delete deployment-demo-1
```

## What is AWS CloudFormation

| solution | type | language |
|---:|:---:|:---|
| Terraform | declarative | `HCL` / `JSON`
| Cloud Formation | declarative | `YAML` / `JSON`

```sh
AWS_PROFILE="MY-PROFILE"

# create stack
aws cloudformation create-stack --stack-name stack-demo-1 --template-body file://demo-01.yaml --profile $AWS_PROFILE

# update stack
aws cloudformation update-stack --stack-name stack-demo-1 --template-body file://demo-01.yaml --profile $AWS_PROFILE

# delete stack
aws cloudformation delete-stack --stack-name stack-demo-1 --profile $AWS_PROFILE

# create a preview change
aws cloudformation create-change-set --stack-name stack-demo-1 --change-set-name preview-changes --template-body file://demo-01.yaml --profile $AWS_PROFILE

# delete a preview change
aws cloudformation delete-change-set --stack-name stack-demo-1 --change-set-name preview-changes --profile $AWS_PROFILE

# view a preview change
aws cloudformation describe-change-set --stack-name stack-demo-1 --change-set-name preview-changes --profile $AWS_PROFILE
```

# Cloud Development Manager versus Terraform

Consider the following example:

```terraform
provider "google" {}

resource "google_compute_network" "vpc_network" {
  name                    = "my_vpc-tf"
  auto_create_subnetworks = false
}
```

In order to use Terraform for GCP we create a service account with the following `Compute Network Admin` role.

For simplicity, download the JSON credentials from the service account and set the following environment variables:

```bash
export GOOGLE_CREDENTIALS=serviceaccount-credentials.json
export GOOGLE_PROJECT=project-id
export GOOGLE_REGION=desired-region
export GOOGLE_ZONE=desired-zone
```

> The role has to have the `compute.networks.create` permission in order for `terraform apply` to be allowed CRUD operations for this particular type of resource.
>
> Forbidden error example: 
>
> `Error: Error creating Network: googleapi: Error 403: Required 'compute.networks.create' permission for 'projects/my-project-id/global/networks/my_vpc-tf', forbidden ...`

Running the `terraform plan` will print the following result:
```sh
------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_network.vpc_network will be created
  + resource "google_compute_network" "my_vpc" {
      + auto_create_subnetworks         = false
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + ipv4_range                      = (known after apply)
      + name                            = "my_vpc-tf"
      + project                         = (known after apply)
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------
```

# AWS CloudFormation versus Terraform

# Other solutions

- [Red Hat Ansible](#link-ansible)

# Links

- <a name="link-terraform">[Hashicorp Terraform](www.terraform.io)</a>
- <a name="cloud-deployment-manager">[GCP Cloud Deployment Manager](https://cloud.google.com/deployment-manager/)</a>
- <a name="cloudformation">[AWS CloudFormation](https://aws.amazon.com/cloudformation/)</a>
- <a name="link-tfenv">[`tfenv` CLI](https://github.com/tfutils/tfenv)
- <a name="link-ansible">[Red Hat Ansible](https://www.ansible.com)</a>