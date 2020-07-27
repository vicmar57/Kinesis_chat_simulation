resource "aws_kinesis_stream" "new_stream" {
  name             = "Lobby"
  shard_count      = 1
}