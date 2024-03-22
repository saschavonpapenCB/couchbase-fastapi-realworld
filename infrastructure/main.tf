output "app_url" {
  value = aws_alb.application_load_balancer.dns_name
}


resource "aws_security_group" "service_security_group" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    # Only allowing traffic in from the load balancer security group
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_ecs_service" "app_service" {
  for_each = toset(var.repository_list)

  name            = "${each.key}-service"
  cluster         = "${aws_ecs_cluster.cluster[each.key].id}"
  task_definition = "${aws_ecs_task_definition.app_task[each.key].arn}"
  launch_type     = "FARGATE"
  desired_count   = 3

  load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group.arn}"
    container_name   = "${aws_ecs_task_definition.app_task[each.key].family}"
    container_port   = 5000
  }

  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
    assign_public_ip = true # Provide the containers with public IPs
    security_groups  = ["${aws_security_group.service_security_group.id}"]
  }
}


resource "aws_default_vpc" "default_vpc" {
}


resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "ap-southeast-1a"
}


resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "ap-southeast-1b"
}


resource "aws_alb" "application_load_balancer" {
  name               = "app-load-balancer"
  load_balancer_type = "application"
  subnets = [
    "${aws_default_subnet.default_subnet_a.id}",
    "${aws_default_subnet.default_subnet_b.id}"
  ]
  security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
}


resource "aws_security_group" "load_balancer_security_group" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow traffic in from all sources
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = "${aws_default_vpc.default_vpc.id}" # default VPC
}


resource "aws_lb_listener" "listener" {
  load_balancer_arn = "${aws_alb.application_load_balancer.arn}" #  load balancer
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.target_group.arn}" # target group
  }
}


resource "aws_ecs_cluster" "cluster" {
  for_each = toset(var.repository_list)
  name = each.key
}

resource "aws_ecs_task_definition" "app_task" {
  for_each = toset(var.repository_list)
  family                   = "api-task"
  container_definitions    = <<DEFINITION
  [
    {
      "name": "api-task",
      "image": "${aws_ecr_repository.repository[each.key].repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] # use Fargate as the launch type
  network_mode             = "awsvpc"    # add the AWS VPN network mode as this is required for Fargate
  memory                   = 512         # Specify the memory the container requires
  cpu                      = 256         # Specify the CPU the container requires
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}


resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


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