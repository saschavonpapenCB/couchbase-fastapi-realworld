variable "region" {
    description = "AWS region to create resources in"
    type = string
    default = "ap-southeast-1"
}

variable "repository_list" {
    description = "List of repositories"
    type = list
    default = ["api"]
}