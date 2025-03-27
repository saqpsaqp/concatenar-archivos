#---------------------------------------
# data.tf
#---------------------------------------
# Obtain AWS Account ID
data "aws_caller_identity" "current" {}

data "aws_canonical_user_id" "current" {}

#---------------------------------------
# outputs.tf
#---------------------------------------
output "main_dns_name" {
  value = aws_route53_zone.main.name
}

output "secondary_dns_names" {
  value = aws_route53_zone.secondary[*].name
}

output "main_dns_zone_id" { 
  value = aws_route53_zone.main.zone_id
}

output "secondary_dns_zone_ids" {
  value = aws_route53_zone.secondary[*].zone_id
}


#---------------------------------------
# route53.tf
#---------------------------------------
# Zona DNS para adaggio.io
resource "aws_route53_zone" "main" {
  name = var.main_dns_zone

  tags = merge({
    Name = "${var.prefix}-${var.environment}-principal-zone"
  }, var.tags)

}

# Zonas DNS secundarias
resource "aws_route53_zone" "secondary" {
    count = length(var.secondary_dns_zones)
    name  = element(var.secondary_dns_zones, count.index)

    tags = merge({
        Name = "${var.prefix}-${var.environment}-secondary-zone-${count.index}"
    }, var.tags)
}

#---------------------------------------
# states.tf
#---------------------------------------
terraform {
  required_version = "1.8.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket  = "funnelhot-shared-terraform-us-east-1-203918884146"
    encrypt = true
    key     = "shared/general/terraform.tfstate"
    region  = "us-east-1"
    profile = "funnelhot-shared"
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = var.profile
}

#---------------------------------------
# variables.tf
#---------------------------------------
variable "region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
  default     = "all"
}

variable "profile" {
  description = "Profile para desplegar (.aws/credentials)"
  type        = string
  default     = "funnelhot-shared"
}

variable "tags" {
  description = "Tags for Project"
  type        = map(string)
  default = {
    "project"     = "funnelhot"
    "environment" = "all"
    "component"   = "general"
    "Terraform"   = true
  }
}

variable "prefix" {
  description = "Prefijo para todos los recursos"
  type        = string
  default     = "shared"
}

variable "main_dns_zone" {
  description = "Zona DNS principal"
  type        = string
  default     = "funnelhot.com"  
}


variable "secondary_dns_zones" {
  description = "Zonas DNS Secundarios"
  type        = list(string)
  default     = [
    "accesosecreto.com",
    "aularevelada.com",
    #"videoconfidencial.com",
    #"claserevelada.com",
    #"contenidoinedito.com",
    #"clasevip.com",
  ]
}

