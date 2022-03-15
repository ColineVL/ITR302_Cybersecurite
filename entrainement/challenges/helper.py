def readLine(r):
    serverLine = r.readline()
    print(f"Server: {serverLine.decode().strip()}")
    return serverLine
