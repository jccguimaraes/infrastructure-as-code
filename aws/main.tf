terraform {
  required_version = "0.12.21"

  backend "local" {
    path = "state/terraform.tfstate"
  }
}

variable "credentials" {
  default = "~/.aws/credentials"
}

variable "profile" {
  default = "awsjoao"
}

variable "region" {
  default = "eu-west-3"
}

provider "aws" {
  shared_credentials_file = var.credentials
  region                  = var.region
  profile                 = var.profile
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "my-vpc-tf"
  }
}