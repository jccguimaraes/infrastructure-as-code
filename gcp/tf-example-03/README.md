# Terraform Google - Step 3

This iteration consists on adding a subnetwork `my_subnet` to an already existing vpc `my_vpc` as the previous [Step 2](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-02) with the exception that we now want to manage the `my_vpc`, in other words, change from a data object to a resource object.

This would allow us to make changes to `my_vpc` or even destroy it.

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

resource "google_compute_network" "my_vpc" {
  name = "my_vpc"
}

resource "google_compute_subnetwork" "my_subnet" {
  name          = "my_subnet"
  ip_cidr_range = "10.2.0.0/16"
  network       = "https://www.googleapis.com/compute/v1/projects/${data.google_project.project.project_id}/global/networks/${google_compute_network.my_vpc.name}"
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

  # google_compute_network.my_vpc will be created
  + resource "google_compute_network" "my_vpc" {
      + auto_create_subnetworks         = true
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + ipv4_range                      = (known after apply)
      + name                            = "my_vpc"
      + project                         = (known after apply)
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

  # google_compute_subnetwork.my_subnet will be created
  + resource "google_compute_subnetwork" "my_subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my_subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc"
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

  # google_compute_network.my_vpc will be created
  + resource "google_compute_network" "my_vpc" {
      + auto_create_subnetworks         = true
      + delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      + id                              = (known after apply)
      + ipv4_range                      = (known after apply)
      + name                            = "my_vpc"
      + project                         = (known after apply)
      + routing_mode                    = (known after apply)
      + self_link                       = (known after apply)
    }

  # google_compute_subnetwork.my_subnet will be created
  + resource "google_compute_subnetwork" "my_subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my_subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc"
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

google_compute_network.my_vpc: Creating...

Error: Error creating Network: googleapi: Error 409: The resource 'projects/personal-265109/global/networks/my_vpc' already exists, alreadyExists

  on main.tf line 13, in resource "google_compute_network" "my_vpc":
  13: resource "google_compute_network" "my_vpc" {
</pre>

> If for some reason, the `my_subnet` creation happened first, that subnet would be created on the existing `my_vpc` and the error would occur as well. Bottom line, there would be **NO ROLLBACK**. Keep in mind that planing sometimes does not mean the apply will run smooth.

So how can we do to achieve this ownership take over?

We need to import the resource into the state by running:

```bash
terraform import google_compute_network.my_vpc projects/personal-265109/global/networks/my_vpc
```

> Take notices that we are setting the already defined resource `google_compute_network.my_vpc` to match the created `my_vpc` id.

This will give us the following output.

<pre>
google_compute_network.my_vpc: Importing from ID "projects/personal-265109/global/networks/my_vpc"...
google_compute_network.my_vpc: Import prepared!
  Prepared google_compute_network for import
google_compute_network.my_vpc: Refreshing state... [id=projects/personal-265109/global/networks/my_vpc]

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
google_compute_network.my_vpc: Refreshing state... [id=projects/personal-265109/global/networks/my_vpc]

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # google_compute_network.my_vpc must be replaced
-/+ resource "google_compute_network" "my_vpc" {
      ~ auto_create_subnetworks         = false -> true # forces replacement
        delete_default_routes_on_create = false
      + gateway_ipv4                    = (known after apply)
      ~ id                              = "projects/personal-265109/global/networks/my_vpc" -> (known after apply)
      + ipv4_range                      = (known after apply)
        name                            = "my_vpc"
      ~ project                         = "personal-265109" -> (known after apply)
      ~ routing_mode                    = "REGIONAL" -> (known after apply)
      ~ self_link                       = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc" -> (known after apply)

      - timeouts {}
    }

  # google_compute_subnetwork.my_subnet will be created
  + resource "google_compute_subnetwork" "my_subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my_subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc"
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
resource "google_compute_network" "my_vpc" {
  name = "my_vpc"
  auto_create_subnetworks = false
}
```

This will give the following output from `terraform plan``

<pre>
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.google_project.project: Refreshing state...
google_compute_network.my_vpc: Refreshing state... [id=projects/personal-265109/global/networks/my_vpc]

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_compute_subnetwork.my_subnet will be created
  + resource "google_compute_subnetwork" "my_subnet" {
      + creation_timestamp = (known after apply)
      + enable_flow_logs   = (known after apply)
      + fingerprint        = (known after apply)
      + gateway_address    = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.2.0.0/16"
      + name               = "my_subnet"
      + network            = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc"
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

If we didn't do this change, `terraform apply` would recreate the `my_vpc` with the default values, which would generate subnetworks for all regions available **BUT** most important, it would add also our own subnetwork. Meaning we would have 2 subnets for the region `europe-west3` as the following image proves it.

> Note that when we imported the vpc, it's ID was nothing more than the name of the vpc itself!

![step-1][step-1]

Since we now took ownership of the `my_vpc` and we also manage `my_subnet`, we can delete both resources. `terraform destroy` will output the following:

<pre>
data.google_project.project: Refreshing state...
google_compute_network.my_vpc: Refreshing state... [id=projects/personal-265109/global/networks/my_vpc]
google_compute_subnetwork.my_subnet: Refreshing state... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_compute_network.my_vpc will be destroyed
  - resource "google_compute_network" "my_vpc" {
      - auto_create_subnetworks         = false -> null
      - delete_default_routes_on_create = false -> null
      - id                              = "projects/personal-265109/global/networks/my_vpc" -> null
      - name                            = "my_vpc" -> null
      - project                         = "personal-265109" -> null
      - routing_mode                    = "REGIONAL" -> null
      - self_link                       = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc" -> null

      - timeouts {}
    }

  # google_compute_subnetwork.my_subnet will be destroyed
  - resource "google_compute_subnetwork" "my_subnet" {
      - creation_timestamp       = "2020-03-14T11:48:45.150-07:00" -> null
      - gateway_address          = "10.2.0.1" -> null
      - id                       = "projects/personal-265109/regions/europe-west3/subnetworks/my_subnet" -> null
      - ip_cidr_range            = "10.2.0.0/16" -> null
      - name                     = "my_subnet" -> null
      - network                  = "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my_vpc" -> null
      - private_ip_google_access = false -> null
      - project                  = "personal-265109" -> null
      - region                   = "europe-west3" -> null
      - secondary_ip_range       = [] -> null
      - self_link                = "https://www.googleapis.com/compute/v1/projects/personal-265109/regions/europe-west3/subnetworks/my_subnet" -> null
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_compute_subnetwork.my_subnet: Destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet]
google_compute_subnetwork.my_subnet: Still destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet, 10s elapsed]
google_compute_subnetwork.my_subnet: Destruction complete after 17s
google_compute_network.my_vpc: Destroying... [id=projects/personal-265109/global/networks/my_vpc]
google_compute_network.my_vpc: Still destroying... [id=projects/personal-265109/global/networks/my_vpc, 10s elapsed]
google_compute_network.my_vpc: Destruction complete after 17s

Destroy complete! Resources: 2 destroyed.
</pre>

[step-1]: ./assets/step-1.jpg "step 1"