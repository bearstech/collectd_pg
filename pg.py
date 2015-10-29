import psycopg2 as pg


COLUMNS = map(lambda a: a.strip(), "datid |    datname    | numbackends | xact_commit | xact_rollback | blks_read | blks_hit  | tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files | temp_bytes  | deadlocks | blk_read_time | blk_write_time |          stats_reset".split("|"))


def stats(url):
    conn = pg.connect(url)
    cur = conn.cursor()
    cur.execute("""SELECT *
                FROM pg_stat_database
                WHERE datname NOT LIKE 'template%' ORDER BY datname;""")
    for line in cur:
        yield dict(zip(COLUMNS, line))


if __name__ == "__main__":
    import sys
    for stat in stats(sys.argv[1]):
        print(stat)
