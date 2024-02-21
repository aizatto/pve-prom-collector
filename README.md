# Proxmox Virtual Environment (PVE) Prom Collector

Make available proxmox cluster information to Prometheus through node-exporter.

## Prerequisite

Test that you can get cluster information on your proxmox server.

On your proxmos server execute the following and observe it is successful.
```sh
pvesh get /cluster/resources --output-format json
```

## Installation

Copy the script over to your proxmox server

Option 1: `curl`

```sh
curl -o /usr/local/bin/pve-prom-collector.py https://raw.githubusercontent.com/aizatto/pve-prom-collector/main/pve-prom-collector.py
```

Option 2: `scp`

```sh
scp pve-collector.py pve:/usr/local/bin/pve-prom-collector.py
```

Test that it works
```sh
pvesh get /cluster/resources --output-format json | python3 /usr/local/bin/pve-prom-collector.py
```

Test that you can write to the `node-exporter directory`
```sh
pvesh get /cluster/resources --output-format json | python3 /usr/local/bin/pve-prom-collector.py | sponge /var/lib/prometheus/node-exporter/pve.prom
```

Observe file is successfully written
```sh
cat /var/lib/prometheus/node-exporter/pve.prom
```

Observe it appears in metrics endpoint
```sh
curl http://localhost/metrics | grep pve_up
```

Install into cron
```sh
crontab -e
```

```sh
* * * * *   pvesh get /cluster/resources --output-format json | python3 /usr/local/bin/pve-prom-collector.py | sponge /var/lib/prometheus/node-exporter/pve.prom
```

```sh
ls /var/lib/prometheus/node-exporter/
```

### Optional: Install Grafana Dashboard

1. [Proxmox via Prometheus](https://grafana.com/grafana/dashboards/10347-proxmox-via-prometheus/)

## Background

I wanted a means to export proxmox information into Prometheus, and I couldn't find a means to.

I am no means an expert in Python, Proxmox, Prometheus, Grafana, or Node Exporter.

I discovered [Prometheus Proxmox VE Exporter](https://github.com/prometheus-pve/prometheus-pve-exporter) but it hosted a webserver for prometheus to pull data from. I wanted something simpler lowering my surface area of attack, and that already worked with `node-exporter`s text-collector.

### Inspired by

1. [Prometheus Proxmox VE Exporter](https://github.com/prometheus-pve/prometheus-pve-exporter)
2. [lvm-prom-collector](https://github.com/prometheus-community/node-exporter-textfile-collector-scripts/blob/master/lvm-prom-collector)

## References

1. [pvesh](https://pve.proxmox.com/pve-docs/pvesh.1.html)
1. [prometheus exposition format](https://github.com/prometheus/docs/blob/main/content/docs/instrumenting/exposition_formats.md#text-format-example)

## Data Type

| Metric Name                | Type  | Help                                                  | Example                                                                                                                                                                                                                                                                                                                                                       |
|----------------------------|-------|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pve_up                     | gauge | Node/VM/CT-Status is online/running                   | pve_up{id="node/pve"} 1.0<br>pve_up{id="lxc/101"} 0.0<br>pve_up{id="lxc/102"} 1.0                                                                                                                                                                                                                                                                             |
| pve_disk_size_bytes        | gauge | Size of storage device                                | pve_disk_size_bytes{id="lxc/100"} 9.126805504e+09<br>pve_disk_size_bytes{id="lxc/101"} 8.589934592e+09<br>pve_disk_size_bytes{id="lxc/102"} 2.2081499136e+010<br>pve_disk_size_bytes{id="node/pve"} 1.0086172672e+011<br>pve_disk_size_bytes{id="storage/pve/local"} 1.0086172672e+011<br>pve_disk_size_bytes{id="storage/pve/local-lvm"} 1.836111101952e+012 |
| pve_disk_usage_bytes       | gauge | Disk usage in bytes                                   | pve_disk_usage_bytes{id="lxc/100"} 0.0<br>pve_disk_usage_bytes{id="lxc/101"} 0.0<br>pve_disk_usage_bytes{id="lxc/102"} 1.5069761536e+010<br>pve_disk_usage_bytes{id="node/pve"} 4.203134976e+09<br>pve_disk_usage_bytes{id="storage/pve/local"} 4.203134976e+09<br>pve_disk_usage_bytes{id="storage/pve/local-lvm"} 1.7626666578e+010                         |
| pve_memory_size_bytes      | gauge | Size of memory                                        | pve_memory_size_bytes{id="lxc/100"} 1.073741824e+09<br>pve_memory_size_bytes{id="lxc/101"} 8.589934592e+09<br>pve_memory_size_bytes{id="lxc/102"} 1.7179869184e+010<br>pve_memory_size_bytes{id="node/pve"} 3.3422065664e+010                                                                                                                                 |
| pve_memory_usage_bytes     | gauge | Memory usage in bytes                                 | pve_memory_usage_bytes{id="lxc/100"} 0.0<br>pve_memory_usage_bytes{id="lxc/101"} 0.0<br>pve_memory_usage_bytes{id="lxc/102"} 2.73381376e+09<br>pve_memory_usage_bytes{id="node/pve"} 4.297396224e+09                                                                                                                                                          |
| pve_network_transmit_bytes | gauge | Number of bytes transmitted over the network          | pve_network_transmit_bytes{id="lxc/100"} 0.0<br>pve_network_transmit_bytes{id="lxc/101"} 0.0<br>pve_network_transmit_bytes{id="lxc/102"} 8.71139672e+08                                                                                                                                                                                                       |
| pve_network_receive_bytes  | gauge | Number of bytes received over the network             | pve_network_receive_bytes{id="lxc/100"} 0.0<br>pve_network_receive_bytes{id="lxc/101"} 0.0<br>pve_network_receive_bytes{id="lxc/102"} 2.206799433e+09                                                                                                                                                                                                         |
| pve_disk_write_bytes       | gauge | Number of bytes written to storage                    | pve_disk_write_bytes{id="lxc/100"} 0.0<br>pve_disk_write_bytes{id="lxc/101"} 0.0<br>pve_disk_write_bytes{id="lxc/102"} 1.37592832e+08                                                                                                                                                                                                                         |
| pve_disk_read_bytes        | gauge | Number of bytes read from storage                     | pve_disk_read_bytes{id="lxc/100"} 0.0<br>pve_disk_read_bytes{id="lxc/101"} 0.0<br>pve_disk_read_bytes{id="lxc/102"} 7.54520064e+08                                                                                                                                                                                                                            |
| pve_cpu_usage_ratio        | gauge | CPU usage (value between 0.0 and pve_cpu_usage_limit) | pve_cpu_usage_ratio{id="lxc/100"} 0.0<br>pve_cpu_usage_ratio{id="lxc/101"} 0.0<br>pve_cpu_usage_ratio{id="lxc/102"} 0.0287861703119817<br>pve_cpu_usage_ratio{id="node/pve"} 0.0144081480561421                                                                                                                                                               |
| pve_cpu_usage_limit        | gauge | Maximum allowed CPU usage                             | pve_cpu_usage_limit{id="lxc/100"} 1.0<br>pve_cpu_usage_limit{id="lxc/101"} 1.0<br>pve_cpu_usage_limit{id="lxc/102"} 4.0<br>pve_cpu_usage_limit{id="node/pve"} 8.0                                                                                                                                                                                             |
| pve_uptime_seconds         | gauge | Number of seconds since the last boot                 | pve_uptime_seconds{id="lxc/100"} 0.0<br>pve_uptime_seconds{id="lxc/101"} 0.0<br>pve_uptime_seconds{id="lxc/102"} 246808.0<br>pve_uptime_seconds{id="node/pve"} 342781.0                                                                                                                                                                                       |
| pve_storage_shared         | gauge | Number of seconds since the last boot                 | pve_storage_shared{id="storage/pve/local"} 0.0<br>pve_storage_shared{id="storage/pve/local-lvm"} 0.0                                                                                                                                                                                                                                                          |
| pve_guest_info             | gauge | VM/CT info                                            | pve_guest_info{id="lxc/100",name="alpine",node="pve",type="lxc"} 1.0<br>pve_guest_info{id="lxc/101",name="ubuntu",node="pve",type="lxc"} 1.0<br>pve_guest_info{id="lxc/102",name="fedora",node="pve",type="lxc"} 1.0                                                                                                                                          |
| pve_storage_info           | gauge | Storage info                                          | pve_storage_info{id="storage/pve/local",node="pve",storage="local"} 1.0<br>pve_storage_info{id="storage/pve/local-lvm",node="pve",storage="local-lvm"} 1.0                                                                                                                                                                                                    |
| pve_node_info              | gauge | Node info                                             | pve_node_info{id="node/pve",level="",name="pve",nodeid="0"} 1.0                                                                                                                                                                                                                                                                                               |
| pve_version_info           | gauge | Proxmox VE version info                               | pve_version_info{release="8.0",repoid="bbf3993334bfa916",version="8.0.3"} 1.0                                                                                                                                                                                                                                                                                 |
| pve_onboot_status          | gauge | Proxmox vm config onboot value                        | pve_onboot_status{id="lxc/102",node="pve",type="lxc"} 1.0                                                                                                                                                                                                                                                                                                     |
