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
  # auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "my_subnet" {
  name          = "my_subnet"
  ip_cidr_range = "10.2.0.0/16"
  network       = "https://www.googleapis.com/compute/v1/projects/${data.google_project.project.project_id}/global/networks/${google_compute_network.my_vpc.name}"
}