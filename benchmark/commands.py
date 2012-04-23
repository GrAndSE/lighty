def benchmark():
    '''Run benchmark
    '''
    import os
    import sys
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))

    import simple
    import iftag
    import fortag
