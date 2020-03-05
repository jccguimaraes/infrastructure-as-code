# Terraform Google - Step 2

This iteration consists on adding a subnetwork `my-subnet` to an already existing vpc `my-vpc` as the previous [Step 1](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-01) with the exception we are using a data object to reference the `my-vpc` resource.

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

data "google_compute_network" "my-vpc" {
  name = "my-vpc"
}

resource "google_compute_subnetwork" "my-subnet" {
  name          = "my-subnet"
  ip_cidr_range = "10.2.0.0/16"
  network       = "https://www.googleapis.com/compute/v1/projects/${data.google_project.project.project_id}/global/networks/${data.google_compute_network.my-vpc.name}"
}
```

Running `terraform init`, `terraform plan`, `terraform apply` and `terraform delete` will result in the same outputs as from [Step 1](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-01).

Next go to [Step 3](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/tf-example-03)!