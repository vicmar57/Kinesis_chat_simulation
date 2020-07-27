# _provider.tf
provider "aws" {
  region = "us-east-1" 
}

provider "aws" {
  alias  = "us-west-1"
  region = "us-west-1"
}

provider "aws" {
	alias  = "eu-west-1"
	region = "eu-west-1" 
}