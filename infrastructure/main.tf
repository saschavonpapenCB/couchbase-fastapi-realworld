
data "aws_caller_identity" "current" {}

resource "aws_ecs_service" "cypress" {
  name            = "cypress-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.cypress.arn
  desired_count   = var.cypress_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnets
    security_groups = var.security_groups
  }
}

resource "aws_ecs_service" "backend" {
  name            = "backend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = var.backend_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnets
    security_groups = var.security_groups
  }
}

resource "aws_ecs_service" "frontend" {
  name            = "frontend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = var.frontend_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnets
    security_groups = var.security_groups
  }
}

resource "aws_ecs_task_definition" "backend" {
  family                = "backend-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.backend_task_cpu
  memory                = var.backend_task_memory

  container_definitions = jsonencode([
    {
      name      = "backend-container"
      image     = "${aws_ecr_repository.backend.repository_url}:${var.backend_image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = var.backend_container_port
          hostPort      = var.backend_host_port
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "frontend" {
  family                = "frontend-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.frontend_task_cpu
  memory                = var.frontend_task_memory

  container_definitions = jsonencode([
    {
      name      = "frontend-container"
      image     = "${aws_ecr_repository.frontend.repository_url}:${var.frontend_image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = var.frontend_container_port
          hostPort      = var.frontend_host_port
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "cypress" {
  family                = "cypress-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.cypress_task_cpu
  memory                = var.cypress_task_memory

  container_definitions = jsonencode([
    {
      name      = "cypress-container"
      image     = "${aws_ecr_repository.cypress.repository_url}:${var.cypress_image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = var.cypress_container_port
          hostPort      = var.cypress_host_port
        }
      ]
    }
  ])
}

resource "aws_ecs_cluster" "main" {
  name = var.ecs_cluster_name
}

# tfsec:ignore:aws-ecr-repository-customer-key
resource "aws_ecr_repository" "backend" {
  name                 = var.backend_repository_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = var.frontend_repository_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_repository" "cypress" {
  name                 = var.cypress_repository_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name
  policy     = templatefile(var.lifecycle_policy, {})
}

resource "aws_ecr_lifecycle_policy" "frontend" {
  repository = aws_ecr_repository.frontend.name
  policy     = templatefile(var.lifecycle_policy, {})
}

resource "aws_ecr_lifecycle_policy" "cypress" {
  repository = aws_ecr_repository.cypress.name
  policy     = templatefile(var.lifecycle_policy, {})
}

resource "aws_ecr_registry_scanning_configuration" "scan_configuration" {
  scan_type = "ENHANCED"

  rule {
    scan_frequency = "CONTINUOUS_SCAN"
    repository_filter {
      filter      = "*"
      filter_type = "WILDCARD"
    }
  }
}
