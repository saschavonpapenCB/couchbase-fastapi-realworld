
data "aws_caller_identity" "current" {}

resource "aws_ecs_service" "cypress" {
  name            = "cypress-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.cypress.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.service_subnets
    security_groups = var.service_security_groups
  }
}

resource "aws_ecs_service" "backend" {
  name            = "backend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.service_subnets
    security_groups = var.service_security_groups
  }
}

resource "aws_ecs_service" "frontend" {
  name            = "frontend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.service_subnets
    security_groups = var.service_security_groups
  }
}

resource "aws_ecs_task_definition" "backend" {
  family                = "backend-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.task_cpu
  memory                = var.task_memory

  container_definitions = jsonencode([
    {
      name      = "backend-container"
      image     = "${aws_ecr_repository.backend.repository_url}:${var.backend_image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "frontend" {
  family                = "frontend-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.task_cpu
  memory                = var.task_memory

  container_definitions = jsonencode([
    {
      name      = "frontend-container"
      image     = "${aws_ecr_repository.frontend.repository_url}:${var.frontend_image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "cypress" {
  family                = "cypress-task"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                   = var.task_cpu
  memory                = var.task_memory

  container_definitions = jsonencode([
    {
      name      = "cypress-container"
      image     = "${aws_ecr_repository.cypress.repository_url}:${var.cypress_image_tag}"
      essential = true
      dependsOn = [
        {
          containerName = "frontend-container"
          condition     = "START"
        },
        {
          containerName = "backend-container"
          condition     = "START"
        }
      ]
      volumes = [
        {
          host = {
            sourcePath = "/frontend"
          }
          containerPath = "/e2e"
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
