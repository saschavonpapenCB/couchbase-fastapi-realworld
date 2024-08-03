variable "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  type        = string
  
}

variable "cypress_task_cpu" {
  description = "The CPU units to allocate for the testing task"
  type        = string
}

variable "cypress_task_memory" {
  description = "The memory in MiB to allocate for the testing task"
}

variable "cypress_container_port" {
  description = "The container port for the testing service"
  type        = number
}

variable "cypress_host_port" {
  description = "The host port for the testing service"
  type        = number
}

variable "backend_task_cpu" {
  description = "The CPU units to allocate for the backend task"
  type        = string
}

variable "backend_task_memory" {
  description = "The memory in MiB to allocate for the backend task"
  type        = string
}

variable "backend_container_port" {
  description = "The container port for the backend service"
  type        = number
}

variable "backend_host_port" {
  description = "The host port for the backend service"
  type        = number
}

variable "frontend_task_cpu" {
  description = "The CPU units to allocate for the frontend task"
  type        = string
}

variable "frontend_task_memory" {
  description = "The memory in MiB to allocate for the frontend task"
}

variable "frontend_container_port" {
  description = "The container port for the frontend service"
  type        = number
}

variable "frontend_host_port" {
  description = "The host port for the frontend service"
  type        = number
}

variable "cypress_desired_count" {
  description = "The desired count of testing tasks"
  type        = number
}

variable "backend_desired_count" {
  description = "The desired count of backend tasks"
  type        = number
}

variable "frontend_desired_count" {
  description = "The desired count of frontend tasks"
  type        = number
}

variable "subnets" {
  description = "The subnets to deploy the ECS services into"
  type        = list(string)
}

variable "security_groups" {
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