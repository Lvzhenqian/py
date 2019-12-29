import docker


client = docker.DockerClient(base_url="tcp://10.0.2.15:6666",timeout=10)


proxy = client.containers.run(image='tecnativa/tcp-proxy', detach=True,
                                          name="apiserver-proxy",
                                          restart_policy={"Name","always"},
                                          environment={"LISTEN": ":8443",
                                                       "TIMEOUT_TUNNEL":"1800s",
                                                       "TALK": "10.0.2.15:6443"},
                                          ports={'8443/tcp': 8443})
print(proxy.status)