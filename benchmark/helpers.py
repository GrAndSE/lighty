def print_time(name, results):
    print '\n%s:' % name
    for exec_time in results:
        print '   ', exec_time
    print ' ', sum(results) / len(results), '\n'
