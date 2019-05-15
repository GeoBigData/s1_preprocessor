import gbdxtools
import json
import os
import click

@click.command()
@click.argument('task_json')
def main(task_json):
    gbdx = gbdxtools.Interface()

    # register the task on gbdx
    # confirm it exists
    if os.path.exists(task_json):
        gbdx.task_registry.register(json_filename=task_json)
    else:
        raise Exception("File does not exist: {}".format(task_json))

    # extract the task name from the json
    with open(task_json, 'r') as f:
        d = json.load(f)
        task_name = ':'.join([str(d['name']), str(d['version'])])

    # confirm it got added
    print('waiting on task registration within gbdx')
    while task_name not in gbdx.task_registry.list():
        print('.')

    print('task successfully registered')


if __name__ == '__main__':
    main()

