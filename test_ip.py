import psutil

def remote_ips():
    ips = []
    for process in psutil.process_iter():
        try:
            connections = process.net_connections(kind='inet')
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        else:
            for connection in connections:
                if connection.raddr and connection.raddr.ip not in ips:
                    ips.append(connection.raddr.ip)
    return ips

def remote_ip_present(ip):
    return ip in remote_ips()

if __name__ == '__main__':
    print(remote_ips())
    print("Left cam: " + str(remote_ip_present('192.168.0.250')))
    print("Right cam: " + str(remote_ip_present('192.168.0.251')))
