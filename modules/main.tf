
# Create CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "cpu_utilization" {
  for_each = toset(var.brokers)
  alarm_name          = "${var.name} ${var.project} ${each.value} CPU Utilization Exceeds to the threshold"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "SystemCpuUtilization"
  namespace           = "AWS/AmazonMQ"
  period              = "300"
  statistic           = "Average"
  threshold           = var.cpu_utilization_threshold
  alarm_description = "This alarm triggers when CPU utilization exceeds 1%"
  alarm_actions     = [aws_sns_topic.alarm_notifications.arn]
  ok_actions        = [aws_sns_topic.alarm_notifications.arn]
  dimensions = {
    Broker = each.key
  }

}

resource "aws_cloudwatch_metric_alarm" "memory_utilization" {
  for_each = toset(var.brokers)
  alarm_name          = "${var.name} ${var.project} ${each.value} Memory Utilization Exceeds to the threshold"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "RabbitMQMemUsed"
  namespace           = "AWS/AmazonMQ"
  period              = "300"
  statistic           = "Average"
  threshold           = var.memory_utilization_threshold

  alarm_description = "This alarm triggers when Memory utilization exceeds 70%"
  alarm_actions     = [aws_sns_topic.alarm_notifications.arn]
  ok_actions        = [aws_sns_topic.alarm_notifications.arn]

  dimensions = {
    Broker = each.key
  }
}
