import boto3
import click

session = boto3.Session(profile_name='snapshotmanager')
ec2 = session.resource('ec2')


def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances


@click.group()
def cli():
    """Snapshotmanager"""


@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""


@snapshots.command('list')
@click.option('--project', default=None, help='Only snapshots for project (tag Project:<name>)')
def list_snapshots(project):
    "List EC2 snapshots"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    i.id,
                    v.id,
                    s.id,
                    s.state,
                    s.start_time.strftime('%c')
                )))

    return


@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@volumes.command('list')
@click.option('--project', default=None, help='Only volumes for project (tag Project:<name>)')
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
            i.id,
            v.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""


@instances.command('snapshot', help = "Create snapshot of all volumes")
@click.option('--project', default=None, help='Only instance for project (tag Project:<name>)')
def create_snapshots(project):
    "Create snapshot of EC2 instances"


    instances = filter_instances(project)
    for i in instances:
        print('Stopping instance {0} ....'.format(i.id))
        i.stop()  # instance moet eerst gestopt worden om veilig snapshot te maken
        i.wait_until_stopped()
        for v in i.volumes.all():
            print('Creating snapshot of volume {0}'.format(v.id))
            v.create_snapshot('Created by snapshotmanager')
        print('Starting instance {0} ....'.format(i.id))
        i.start()
        i.wait_until_running()

    print('Done')
    return


@instances.command('list')
@click.option('--project', default=None, help='Only instance for project (tag Project:<name>)')
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        print(i)
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Project', '<no project tag>')
        )))

    return


@instances.command('stop')
@click.option('--project', default=None, help='Only instance for project (tag Project:<name>)')
def stop_instances(project):
    "Stop EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        i.stop()

    return


@instances.command('start')
@click.option('--project', default=None, help='Only instance for project (tag Project:<name>)')
def start_instances(project):
    "Start EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))
        i.start()

    return


if __name__ == '__main__':
    cli()
