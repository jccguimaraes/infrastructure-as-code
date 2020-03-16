# Terraform Google - Step 1

This iteration consists on adding a subnetwork `my_subnet` to an already existing vpc `my_vpc`.

This VPC network was created through the GCP console as per the following images.

On the left menu go to `VPC network` and click on the `Create VPC network`.

![step-1][step-1]

Add `my_vpc` as the name and leave the rest as per the next image.

![step-1][step-2]

Validate the vpc was created.

![step-1][step-3]
![step-1][step-4]

Initial setup (will be valid for all other steps / examples):

In order to use Terraform for GCP we create a service account with the following `Compute Network Admin` role.

![step-0-0][step-0-0]
![step-0-1][step-0-1]
![step-0-2][step-0-2]
![step-0-3][step-0-3]

For simplicity, download the JSON credentials from the service account and set the following environment variables:

![step-0-4][step-0-4]

```bash
# set accordingly with your settings
export GOOGLE_CREDENTIALS=path/to/credentials
export GOOGLE_PROJECT=personal-265109
export GOOGLE_REGION=europe-west3
export GOOGLE_ZONE=europe-west3-a
```

This demo has the following Terraform configuration:

```terraform
terraform {
  required_version = "0.12.21"

  backend "local" {
    path = "state/terraform.tfstate"
  }
}

provider "google" {}

data "google_project" "project" {}

resource "google_compute_subnetwork" "my_subnet" {
  name          = "my_subnet"
  ip_cidr_range = "10.2.0.0/16"
  network       = "https://www.googleapis.com/compute/v1/projects/${data.google_project.project.project_id}/global/networks/my_vpc"
}
```

Initialize Terraform with `terraform init`.

<pre>
Initializing the backend...

Successfully configured the backend "local"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "google" (hashicorp/google) 3.12.0...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.google: version = "~> 3.12"

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
</pre>

Make a Terraform plan with `terraform plan` to check what will be created.

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

We hardcoded the name of the vpc that we created before. Next we do `terraform apply` to apply the plan and deploy the subnetwork into `my_vpc`.

<pre>
data.google_project.project: Refreshing state...

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

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_compute_subnetwork.my_subnet: Creating...
google_compute_subnetwork.my_subnet: Still creating... [10s elapsed]
google_compute_subnetwork.my_subnet: Creation complete after 18s [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: state/terraform.tfstate
</pre>

As seen on the console, the `my_subnet` was created under the `my_vpc`.

![step-5][step-5]

You can clean up these changes by running `terraform destroy`:

<pre>
data.google_project.project: Refreshing state...
google_compute_subnetwork.my_subnet: Refreshing state... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_compute_subnetwork.my_subnet will be destroyed
  - resource "google_compute_subnetwork" "my_subnet" {
      - creation_timestamp       = "2020-03-14T10:12:29.047-07:00" -> null
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

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_compute_subnetwork.my_subnet: Destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet]
google_compute_subnetwork.my_subnet: Still destroying... [id=projects/personal-265109/regions/europe-west3/subnetworks/my_subnet, 10s elapsed]
google_compute_subnetwork.my_subnet: Destruction complete after 18s

Destroy complete! Resources: 1 destroyed.
</pre>

Next go to [Step 2](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-02)!

[step-0-0]: ./assets/step-0-0.jpg "step 0-0"
[step-0-1]: ./assets/step-0-1.jpg "step 0-1"
[step-0-2]: ./assets/step-0-2.jpg "step 0-2"
[step-0-3]: ./assets/step-0-3.jpg "step 0-3"
[step-0-4]: ./assets/step-0-4.jpg "step 0-4"
[step-1]: ./assets/step-1.jpg "step 1"
[step-2]: ./assets/step-2.jpg "step 2"
[step-3]: ./assets/step-3.jpg "step 3"
[step-4]: ./assets/step-4.jpg "step 4"
[step-5]: ./assets/step-5.jpg "step 5"