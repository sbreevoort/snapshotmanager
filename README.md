# snapshotmanager
Demo project to manage AWS EC2 instance snapshots with Boto3

## config
uses profile snapshotmanager

## running
`pipenv run python src\snapshotmanager.py <command> <subcommand> <--project=PROJECT>`

*command* is instances, volumes or snapshots
*subcommand* depends on command, e.g. list, start or stop
*project* is optional
