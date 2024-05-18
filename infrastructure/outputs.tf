output "be_ecr_repo_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "be_ecr_repo_arn" {
  value = aws_ecr_repository.backend.arn
}

output "fe_ecr_repo_url" {
  value = aws_ecr_repository.frontend.repository_url
}

output "fe_ecr_repo_arn" {
  value = aws_ecr_repository.frontend.arn
}