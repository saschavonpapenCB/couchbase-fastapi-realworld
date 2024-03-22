resource "aws_ecr_repository" "repository" {
    for_each = toset(var.repository_list)
    name = each.key
}


resource "docker_registry_image" "registry_image" {
    for_each = toset(var.repository_list)
    name          = docker_image.image[each.key].name
    keep_remotely = true
}

resource "docker_image" "image" {
  for_each = toset(var.repository_list)
  name = "${aws_ecr_repository.repository[each.key].repository_url}:latest"

  build {
    context = "../"
    dockerfile = "${each.key}.Dockerfile"
  }
}