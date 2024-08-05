module "mq_alert" {
  source            = "./modules"
  region            = "us-east-1"
  name              = "MQ"
  project           = "Test"
  slack_webhook_url = var.slack_webhook_url
  dimensions = {
    Broker = var.brokers
  }
  brokers                      = var.brokers
  cpu_utilization_threshold    = 60
  memory_utilization_threshold = 70

}

