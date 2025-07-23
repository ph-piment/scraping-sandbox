resource "aws_cloudwatch_event_rule" "weekdays_7pm_jst" {
  name                = "weekdays-7pm-jst"
  description         = "Every weekday at 19:00 JST"
  schedule_expression = "cron(0 10 ? * MON-FRI *)"  # JST19:00 = UTC10:00
}

resource "aws_cloudwatch_event_target" "lambda_trigger" {
  rule      = aws_cloudwatch_event_rule.weekdays_7pm_jst.name
  target_id = "edinet-lambda"
  arn       = aws_lambda_function.notify_big_holders.arn
  input     = jsonencode({ date = "" })
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notify_big_holders.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekdays_7pm_jst.arn
}
