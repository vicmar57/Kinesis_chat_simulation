module "us-east-1" {
  source = "./modules/multi-region"
  providers = {
    aws = "aws"
  }
}

module "us-west-1" {
  source = "./modules/multi-region"
  providers = {
    aws = "aws.us-west-1"
  }
}

module "eu-west-1" {
  source = "./modules/multi-region"
  providers = {
    aws = "aws.eu-west-1"
  }
}