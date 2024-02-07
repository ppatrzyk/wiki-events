variable "hcloud_token" {}

provider "hcloud" {
  token = "${var.hcloud_token}"
}

resource "hcloud_server" "wikievents" {
  name        = "wikievents"
  image       = "ubuntu-22.04"
  server_type = "cx11"
  location = "hel1"
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}