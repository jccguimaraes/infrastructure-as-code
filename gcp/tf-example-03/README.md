# Terraform Google - Step 3

This iteration consists on adding a subnetwork `my-subnet` to an already existing vpc `my-vpc` as the previous [Step 2](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-02) with the exception that we now want to manage the `my-vpc`, in other words, change from a data object to a resource object.

This would allow us to make changes to `my-vpc` or even destroy it.

Consider the following terraform statement:

```terraform
terraform {
  required_version = "0.12.21"

  backend "local" {
    path = "state/terraform.tfstate"
  }
}

provider "google" {}

data "google_project" "project" {}

resource "google_compute_network" "my-vpc" {
  name = "my-vpc"
}

resource "google_compute_subnetwork" "my-subnet" {
  name          = "my-subnet"
  ip_cidr_range = "10.2.0.0/16"
  network       = "https://www.googleapis.com/compute/v1/projects/${data.google_project.project.project_id}/global/networks/${google_compute_network.my-vpc.name}"
}
```

Notice that we changed from a `google_compute_network` data object to a resource one.

Now, if we run `terraform plan` we will get a slightly different result as the previous [Step 2](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-02).

<pre>
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.google_project.project: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_network.my-vpc will be created
  + resource "google_compute_network" "my-vpc" {
      + auto_create_subnetworks         = true
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + ipv4_range                      = (known after apply)
      + name                            = "my-vpc"
      + project                         = (known after apply)
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

  # google_compute_subnetwork.my-subnet will be created
  + resource "google_compute_subnetwork" "my-subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my-subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
      + project            = (known after apply)
      + region             = (known after apply)
      + secondary_ip_range = (known after apply)
      + self_link          = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.
</pre>

Now Terraform will try to create 2 resources, so what will happen if we try to apply this plan?

`terraform apply` and `terraform delete` will cause errors such as the following:

<pre>
ata.google_project.project: Refreshing state...

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_network.my-vpc will be created
  + resource "google_compute_network" "my-vpc" {
      + auto_create_subnetworks         = true
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + ipv4_range                      = (known after apply)
      + name                            = "my-vpc"
      + project                         = (known after apply)
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

  # google_compute_subnetwork.my-subnet will be created
  + resource "google_compute_subnetwork" "my-subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my-subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
      + project            = (known after apply)
      + region             = (known after apply)
      + secondary_ip_range = (known after apply)
      + self_link          = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_compute_network.my-vpc: Creating...

Error: Error creating Network: googleapi: Error 409: The resource 'projects/personal-265109/global/networks/my-vpc' already exists, alreadyExists

  on main.tf line 13, in resource "google_compute_network" "my-vpc":
  13: resource "google_compute_network" "my-vpc" {
</pre>

> If for some reason, the `my-subnet` creation happened first, that subnet would be created on the existing `my-vpc` and the error would occur as well. Bottom line, there would be **NO ROLLBACK**. Keep in mind that planing sometimes does not mean the apply will run smooth.

So how can we do to achieve this ownership take over?

We need to import the resource into the state by running:

```bash
terraform import google_compute_network.my-vpc projects/personal-265109/global/networks/my-vpc
```

> Take notices that we are setting the already defined resource `google_compute_network.my-vpc` to match the created `my-vpc` id.

This will give us the following output.

<pre>
google_compute_network.my-vpc: Importing from ID "projects/personal-265109/global/networks/my-vpc"...
google_compute_network.my-vpc: Import prepared!
  Prepared google_compute_network for import
google_compute_network.my-vpc: Refreshing state... [id=projects/personal-265109/global/networks/my-vpc]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
</pre>

After this step, `terraform plan` will give a strange output:

<pre>
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.google_project.project: Refreshing state...
google_compute_network.my-vpc: Refreshing state... [id=projects/personal-265109/global/networks/my-vpc]

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # google_compute_network.my-vpc must be replaced
-/+ resource "google_compute_network" "my-vpc" {
      ~ auto_create_subnetworks         = false -> true # forces replacement
        delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      ~ id                              = "projects/personal-265109/global/networks/my-vpc" -> (known after apply)
      + ipv4_range                      = (known after apply)
        name                            = "my-vpc"
      ~ project                         = "personal-265109" -> (known after apply)
      ~ routing_mode                    = "REGIONAL" -> (known after apply)
      ~ self_link                       = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc" -> (known after apply)

      - timeouts {}
    }

  # google_compute_subnetwork.my-subnet will be created
  + resource "google_compute_subnetwork" "my-subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my-subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
      + project            = (known after apply)
      + region             = (known after apply)
      + secondary_ip_range = (known after apply)
      + self_link          = (known after apply)
    }

Plan: 2 to add, 0 to change, 1 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.
</pre>

It's deleting and creating the same vpc (kinda)! What is wrong here? Terraform follows the default values for a vpc creation, and since we created a vpc (through the console) with `auto_create_subnetworks` set to `false`, it is defaulting to `true`. On top of this, since GCP does not allow for changing the name, it needs to destroy and create a new vpc.

So change the `google_compute_network` as follows:

```terraform
resource "google_compute_network" "my-vpc" {
  name = "my-vpc"
  auto_create_subnetworks = false
}
```

This will give the following output from `terraform plan``

<pre>
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.google_project.project: Refreshing state...
google_compute_network.my-vpc: Refreshing state... [id=projects/personal-265109/global/networks/my-vpc]

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_subnetwork.my-subnet will be created
  + resource "google_compute_subnetwork" "my-subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my-subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
      + project            = (known after apply)
      + region             = (known after apply)
      + secondary_ip_range = (known after apply)
      + self_link          = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

Note: You didn't specify an "-out" parameter to save this plan, so Terraform
can't guarantee that exactly these actions will be performed if
"terraform apply" is subsequently run.
</pre>

If we didn't do this change, `terraform apply` would recreate the `my-vpc` with the default values, which would generate subnetworks for all regions available **BUT** most important, it would add also our own subnetwork. Meaning we would have 2 subnets for the region `europe-west3` as the following image proves it.

> Note that when we imported the vpc, it's ID was nothing more than the name of the vpc itself!

![step-1][step-1]

Since we now took ownership of the `my-vpc` and we also manage `my-subnet`, we can delete both resources. `terraform destroy` will output the following:

<pre>
data.google_project.project: Refreshing state...
google_compute_network.my-vpc: Refreshing state... [id=projects/personal-265109/global/networks/my-vpc]
google_compute_subnetwork.my-subnet: Refreshing state... [id=projects/personal-265109/regions/europe-west3/subnetworks/my-subnet]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_compute_network.my-vpc will be destroyed
  - resource "google_compute_network" "my-vpc" {
      - auto_create_subnetworks         = false -> null
      - delete_default_routes_on_create = false -> null
      - id                              = "projects/personal-265109/global/networks/my-vpc" -> null
      - name                            = "my-vpc" -> null
      - project                         = "personal-265109" -> null
      - routing_mode                    = "REGIONAL" -> null
      - self_link                       = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc" -> null

      - timeouts {}
    }

  # google_compute_subnetwork.my-subnet will be destroyed
  - resource "google_compute_subnetwork" "my-subnet" {
      - creation_timestamp       = "2020-03-14T11:48:45.150-07:00" -> null
      - gateway_address          = "10.2.0.1" -> null
      - id                       = "projects/personal-265109/regions/europe-west3/subnetworks/my-subnet" -> null
      - ip_cidr_range            = "10.2.0.0/16" -> null
      - name                     = "my-subnet" -> null
      - network                  = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc" -> null
      - private_ip_google_access = false -> null
      - project                  = "personal-265109" -> null
      - region                   = "europe-west3" -> null
      - secondary_ip_range       = [] -> null
      - self_link                = "https://www.googleapis.com/compute/v1/projects/personal-265109/regions/europe-west3/subnetworks/my-subnet" -> null
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_compute_subnetwork.my-subnet: Destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my-subnet]
google_compute_subnetwork.my-subnet: Still destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my-subnet, 10s elapsed]
google_compute_subnetwork.my-subnet: Destruction complete after 17s
google_compute_network.my-vpc: Destroying... [id=projects/personal-265109/global/networks/my-vpc]
google_compute_network.my-vpc: Still destroying... [id=projects/personal-265109/global/networks/my-vpc, 10s elapsed]
google_compute_network.my-vpc: Destruction complete after 17s

Destroy complete! Resources: 2 destroyed.
</pre>

[step-1]: ./assets/step-1.jpg "step 1"