from urlparse import urlparse
import psycopg2


COLUMNS = map(lambda a: a.strip(), "datid |    datname    | numbackends \
| xact_commit | xact_rollback | blks_read | blks_hit  | tup_returned \
| tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts \
| temp_files | temp_bytes  | deadlocks | blk_read_time | blk_write_time \
|          stats_reset".split("|"))


def stats(uri):
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("""SELECT *
                FROM pg_stat_database
                WHERE datname NOT LIKE 'template%' ORDER BY datname;""")
    for line in cur:
        yield dict(zip(COLUMNS, line))

try:
    import collectd
except ImportError:
    # we're not running inside collectd
    # it's ok
    pass
else:

    def logger(t, msg):
        if t == 'err':
            collectd.error('%s: %s' % (NAME, msg))
        elif t == 'warn':
            collectd.warning('%s: %s' % (NAME, msg))
        elif t == 'info':
            collectd.info('%s: %s' % (NAME, msg))
        else:
            collectd.notice('%s: %s' % (NAME, msg))

    NAME = "pg"
    uris = []

    def config_callback(conf):
        global uris
        for node in conf.children:
            if node.key == "uri":
                uris += node.values
            else:
                logger('warn', "Unknown config %s" % node.key)

    def read_callback():
        global uris
        for uri in uris:
            server = urlparse(uri).hostname
            for stat in stats(uri):
                for v in ['xact_commit', 'xact_rollback', 'blks_read',
                          'blks_hit', 'tup_returned', 'tup_fetched',
                          'tup_inserted', 'tup_updated', 'tup_deleted',
                          'conflicts', 'temp_files', 'temp_bytes', 'deadlocks',
                          'blk_read_time', 'blk_write_time']:
                    val = collectd.Values(plugin=NAME, type="absolute")
                    val.host = server
                    val.plugin_instance = stat['datname']
                    val.values = [stat[v]]
                    val.type = "absolute"
                    val.type_instance = v
                    val.dispatch()
                val = collectd.Values(plugin=NAME, type="gauge")
                val.host = server
                val.plugin_instance = stat['datname']
                val.values = [stat['numbackends']]
                val.type = "gauge"
                val.type_instance = 'numbackends'
                val.dispatch()

    collectd.register_config(config_callback)
    collectd.register_read(read_callback)


if __name__ == "__main__":
    import sys
    for stat in stats(sys.argv[1]):
        print(stat)
