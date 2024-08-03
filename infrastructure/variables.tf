variable "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  type        = string
  
}

variable "cypress_service_name" {
  description = "The name of the cypress service"
  type        = string
}

variable "frontend_service_name" {
  description = "The name of the frontend service"
  type        = string
}

variable "backend_service_name" {
  description = "The name of the backend service"
  type        = string
}

variable "task_cpu" {
  description = "The CPU units to allocate for the tasks"
  type        = string
}

variable "task_memory" {
  description = "The memory in MiB to allocate for the tasks"
}

variable "service_subnets" {
  description = "The subnets to deploy the ECS services into"
  type        = list(string)
}

variable "service_security_groups" {
  description = "The security groups to assign to the ECS services"
  type        = list(string)
}

variable "cypress_image_tag" {
  description = "The tag of the testing image to deploy"
}

variable "backend_image_tag" {
  description = "The tag of the backend image to deploy"
}

variable "frontend_image_tag" {
  description = "The tag of the frontend image to deploy"
}

variable "backend_repository_name" {
  description = "Name of the backend repo"
  type        = string
}

variable "frontend_repository_name" {
  description = "Name of the frontend repo"
  type        = string
}

variable "cypress_repository_name" {
  description = "Name of the testing repo"
  type        = string
}

variable "iam_role" {
  type        = string
  description = "Self-hosted runner EC2 instance role"
}

variable "lifecycle_policy" {
  type        = string
  description = "the lifecycle policy to be applied to the ECR repos"
}

variable "aws_account_id" {
  description = "Target AWS Account ID"
  type        = string
}