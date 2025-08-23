variable "project" { type = string, default = "fiscus-ai" }
variable "aws_region" { type = string, default = "eu-central-1" }
variable "uploads_bucket" { type = string }
variable "domain" { type = string }
variable "enable_logs" { type = bool, default = true }
