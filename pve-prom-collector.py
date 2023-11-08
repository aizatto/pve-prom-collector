import json
import sys

class ClusterResource:
    def __init__(self, data):
        self.__dict__ = data

def run():
    try:
        input_data = read_file_or_stdin()
        resources = json.loads(input_data, object_hook=lambda d: ClusterResource(d))
        output = print_resources(resources)
        print(output)
    except Exception as e:
        print(f"Error: {e}")

def print_resources(resources):
    output = []

    def format_float(num):
        if num == 0:
            return "0.0"

        return "{:9e}".format(num)

    def print_metrics(help_text, type_information, f):
        nonlocal output
        output.append(help_text)
        output.append("\n")
        output.append(type_information)
        output.append("\n")
        for resource in resources:
            try:
                output.append(f(resource))
            except Exception as e:
                print(f"Error processing resource: {e}")

    def format_metric(
        name,
        resource_id,
        value
    ):
        return f'{name}{{id="{resource_id}"}} {value}\n'

    def pve_up_metric(r):
        if r.type not in ('lxc', 'node'):
          return ""
        
        if r.status != 'stopped':
            return format_metric('pve_up', r.id, '1.0')
        else:
            return format_metric('pve_up', r.id, '0.0')

    def pve_disk_size_metric(r):
        if r.type in ('lxc', 'node', 'storage'):
            return format_metric('pve_disk_size_bytes', r.id, format_float(r.maxdisk))
        else:
            return ""

    def pve_disk_usage_metric(r):
        if r.type in ('lxc', 'node', 'storage'):
            return format_metric('pve_disk_usage_bytes', r.id, format_float(r.disk))
        else:
            return ""

    def pve_memory_size_metric(r):
        if r.type in ('lxc', 'node'):
            return format_metric('pve_memory_size_bytes', r.id, format_float(r.maxmem))
        else:
            return ""

    def pve_memory_usage_metric(r):
        if r.type in ('lxc', 'node'):
            return format_metric('pve_memory_usage_bytes', r.id, format_float(r.mem))
        else:
            return ""

    def pve_network_transmit_metric(r):
        if r.type == 'lxc':
            return format_metric('pve_network_transmit_bytes', r.id, format_float(r.netout))
        else:
            return ""

    def pve_network_receive_metric(r):
        if r.type == 'lxc':
            return format_metric('pve_network_receive_bytes', r.id, format_float(r.netin))
        else:
            return ""

    def pve_disk_write_metric(r):
        if r.type == 'lxc':
            return format_metric('pve_disk_write_bytes', r.id, format_float(r.diskwrite))
        else:
            return ""

    def pve_disk_read_metric(r):
        if r.type == 'lxc':
            return format_metric('pve_disk_read_bytes', r.id, format_float(r.diskread))
        else:
            return ""

    def pve_cpu_usage_ratio(r):
        if r.type in ('lxc', 'node'):
            return format_metric('pve_cpu_usage_ratio', r.id, r.cpu)
        else:
            return ""

    def pve_cpu_usage_limit(r):
        if r.type in ('lxc', 'node'):
            return format_metric('pve_cpu_usage_limit', r.id, r.maxcpu)
        else:
            return ""

    def pve_uptime_metric(r):
        if r.type in ('lxc', 'node'):
            return format_metric('pve_uptime_seconds', r.id, r.uptime)
        else:
            return ""

    def pve_guest_info(r):
        if r.type in ('lxc'):
          return f'pve_guest_info{{id="{r.id}",name="{r.name}",node="{r.node}",type="{r.type}"}} 1.0\n'
        else:
            return ""

    def pve_storage_info(r):
        if r.type in ('storage'):
          return f'pve_storage_info{{id="{r.id}",node="{r.node}",storage="{r.storage}"}} 1.0\n'
        else:
            return ""

    def pve_node_info(r):
        if r.type in ('node'):
          return f'pve_node_info{{id="{r.id}",level="{r.level}",name="{r.node}"}} 1.0\n'
        else:
            return ""

    print_metrics(
        "# HELP pve_up Node/VM/CT-Status is online/running",
        "# TYPE pve_up gauge",
        pve_up_metric
    )
    print_metrics(
        "# HELP pve_disk_size_bytes Size of storage device",
        "# TYPE pve_disk_size_bytes gauge",
        pve_disk_size_metric
    )
    print_metrics(
        "# HELP pve_disk_usage_bytes Disk usage in bytes",
        "# TYPE pve_disk_usage_bytes gauge",
        pve_disk_usage_metric
    )
    print_metrics(
        "# HELP pve_memory_size_bytes Size of memory",
        "# TYPE pve_memory_size_bytes gauge",
        pve_memory_size_metric
    )
    print_metrics(
        "# HELP pve_memory_usage_bytes Memory usage in bytes",
        "# TYPE pve_memory_usage_bytes gauge",
        pve_memory_usage_metric
    )
    print_metrics(
        "# HELP pve_network_transmit_bytes Number of bytes transmitted over the network",
        "# TYPE pve_network_transmit_bytes gauge",
        pve_network_transmit_metric
    )
    print_metrics(
        "# HELP pve_network_receive_bytes Number of bytes received over the network",
        "# TYPE pve_network_receive_bytes gauge",
        pve_network_receive_metric
    )
    print_metrics(
        "# HELP pve_disk_write_bytes Number of bytes written to storage",
        "# TYPE pve_disk_write_bytes gauge",
        pve_disk_write_metric
    )
    print_metrics(
        "# HELP pve_disk_read_bytes Number of bytes read from storage",
        "# TYPE pve_disk_read_bytes gauge",
        pve_disk_read_metric
    )
    print_metrics(
        "# HELP pve_cpu_usage_ratio CPU usage (value between 0.0 and pve_cpu_usage_limit)",
        "# TYPE pve_cpu_usage_ratio gauge",
        pve_cpu_usage_ratio
    )
    print_metrics(
        "# HELP pve_cpu_usage_limit Maximum allowed CPU usage",
        "# TYPE pve_cpu_usage_limit gauge",
        pve_cpu_usage_limit
    )
    print_metrics(
        "# HELP pve_uptime_seconds Number of seconds since the last boot",
        "# TYPE pve_uptime_seconds gauge",
        pve_uptime_metric
    )
    print_metrics(
        "# HELP pve_guest_info VM/CT info",
        "# TYPE pve_guest_info gauge",
        pve_guest_info
    )
    print_metrics(
        "# HELP pve_storage_info Storage info",
        "# TYPE pve_storage_info gauge",
        pve_storage_info
    )
    print_metrics(
        "# HELP pve_node_info Node info",
        "# TYPE pve_node_info gauge",
        pve_node_info
    )

    return "".join(output)

def read_file_or_stdin():
    try:
        input_data = ""
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
            input_data = read_file(file_name)
        else:
            while True:
                try:
                    line = input()
                    input_data += line + "\n"
                except EOFError:
                    break
    except Exception as e:
        raise e
    return input_data

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_name}")

if __name__ == "__main__":
    run()
