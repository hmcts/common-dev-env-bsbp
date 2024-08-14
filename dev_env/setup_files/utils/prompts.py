from dev_env.setup_files.utils.utils import query_yes_no


def run_db_only():
    return query_yes_no('%s %s %s' % ('Please choose one of the following.\n',
                                      'Y: you will be using in an IDE to run services (IntelliJ for example).',
                                      'N: you would prefer the script to initialise using Docker.'))
