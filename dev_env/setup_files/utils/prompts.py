from dev_env.setup_files.utils.utils import query_yes_no

def run_db_only():
    return query_yes_no('%s %s' % ('For each service, do you want to only spin up the database?',
            'y = db only, n = all docker services listed in docker compose yml'))
