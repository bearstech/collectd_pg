Collectd Postgres
=================

Yet another Postgres plugin for Collectd.

Configure
---------

For now, it uses [pg_stat_database View](http://www.postgresql.org/docs/9.4/static/monitoring-stats.html#PG-STAT-DATABASE-VIEW), don't forget to configure it.

### Collectd configuration file

    LoadPlugin Python

    <Plugin Python>
        ModulePath "/opt/collectd_cgroups/"
        LogTraces true
        Interactive false
        Import "pg"
        <Module pg>
            uri "postgresql://bob:sponge@localhost/db"
        </Module>
    </Plugin>


Licence
-------

GPLv2, © 2015 Mathieu Lecarme, just like Collectd.
