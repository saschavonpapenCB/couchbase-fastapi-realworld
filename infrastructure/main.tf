
data "aws_caller_identity" "current" {}

# tfsec:ignore:aws-ecr-repository-customer-key
resource "aws_ecr_repository" "backend" {
  name                 = var.backend_repository_name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = var.frontend_repository_name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_repository" "cypress" {
  name                 = var.cypress_repository_name
  image_tag_mutability = "IMMUTABLE"
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
