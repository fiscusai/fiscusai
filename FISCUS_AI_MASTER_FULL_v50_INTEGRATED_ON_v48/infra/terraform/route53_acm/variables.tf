variable "aws_region" {
  description = "AWS region (us-east-1 for ACM/CloudFront)"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Root domain (e.g., fiscus.ai)"
  type        = string
}

variable "hosted_zone_id" {
  description = "Route53 Hosted Zone ID for domain_name"
  type        = string
}
