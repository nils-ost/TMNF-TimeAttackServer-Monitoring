from invoke import task
import os

tmp_dir = '/tmp'
prom_cfg = os.path.join(tmp_dir, 'prometheus.yml')


@task(name='dev-start')
def start_development(c):
    r = c.run('sudo docker ps -f name=dev-prometheus', hide=True)
    if 'dev-prometheus' not in r.stdout:
        tas_ip = input('IP of TAS-Server: ').strip()
        with open('prometheus.yml', 'r') as f:
            prom_yml = f.read()
        prom_yml = prom_yml.replace('##TAS_IP##', tas_ip)
        with open(prom_cfg, 'w') as f:
            f.write(prom_yml)
        print('Starting Prometheus')
        c.run(f'sudo docker run --name dev-prometheus --rm -e TZ=UTC -p 9090:9090 -v {prom_cfg}:/etc/prometheus/prometheus.yml -d ubuntu/prometheus:latest')
    r = c.run('sudo docker ps -f name=dev-grafana', hide=True)
    if 'dev-grafana' not in r.stdout:
        print('Starting Grafana')
        c.run('sudo docker run --name=dev-grafana --rm -p 3000:3000 -d grafana/grafana:8.2.7')


@task(name='dev-stop')
def stop_development(c):
    for name in ['dev-prometheus', 'dev-grafana']:
        r = c.run(f'sudo docker ps -f name={name}', hide=True)
        if name in r.stdout:
            print(f'Stopping {name}')
            c.run(f'sudo docker stop {name}')


@task(pre=[stop_development], post=[start_development], name='dev-clean')
def cleanup_development(c):
    pass
