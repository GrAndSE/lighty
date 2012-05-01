'''This module describes a class for sending and dispatching signals and event.

For example create a signal dispatcher at first::

    dispatcher = SignalDispatcher()

To create new handler function we need to create a channes and add function as
handler to this channel::

    def handler(objects):
        print 'Handle', objects
    dispatcher.channel('/test/', handler)

Then we can send a signal to channel::

    dispatcher.signal('/test/')

This prints 'Handle []'. As you can see we can attach objects into signal to
send messages between different modules::

    dispatcher.signal('/test/', [0, 1, 2, 3])
    
It prints 'Handle [0, 1, 2, 3]'. To add additional options for interactions
between functions we can use filters. Filter provides a way to subscribe
multiply handlers to one channel and pass different objects from signal to
different handler functions::

    def filtered(objects):
        print 'Filtered', objects
    dispatcher.channel('/test/', filtered, filters=[lambda x: x > 0])
    dispatcher.signal('/test/', [0, 1, 2, 3])

This code prints::

    Handle [0, 1, 2, 3]
    Filtered [1, 2, 3]

Filtering can be usefull for impementing the services that derives changes in
entities for different subscribers. As example, Peter and John subscribed for
changes in project. This project has few tickets included. Peter watches for
changes in tickets #1, #2 and #3, and John watches for changes in tickets #2
and #4. Simple code to implement it::

    def send_changes(user, changes):
        pass  # some code to sent changes to user as example vie email

    dispatcher.channel('project', functools.partial(send_changes, 'Peter'),
                       filters=[lambda t: t.ticket_id in [1, 2, 3]])
    dispatcher.channel('project', functools.partial(send_changes, 'John'),
                       filters=[lambda t: t.ticket_id in [2, 4]])
'''
import functools


def check_filters(obj, filters):
    '''Check object with all the filters
    '''
    passing = True
    for f in filters:
        passing &= f(obj)
        if not passing:
            return False
    return True


class SignalDispatcher(object):
    '''Class that routes signals from one from producer to consumer
    '''

    def __init__(self):
        '''Create new signal dispatcher instance with +
        '''
        self.channels = {}

    def channel(self, key, handler, filters=None):
        '''Register new channel for listerning

        Args:
            key - channel key
            handler - handler function
            filters - list of filters for hadnler specified
        '''
        pair = (functools.partial(check_filters, filters=filters)
                if filters else lambda o: True, handler)
        if key not in self.channels:
            self.channels[key] = [pair]
        else:
            self.channels[key].append(pair)

    def signal(self, key, objects=[]):
        '''Proccess a signal for a number of objects
        '''
        if key not in self.channels:
            return
        for filters, handler in self.channels[key]:
            handler([obj for obj in objects if filters(obj)])

    def close(self, key, handler=None):
        '''Close channel or detach handler from channel
        '''
        if handler:
            num = 0
            while num < len(self.channels[key]):
                if self.channels[key][num][1] == handler:
                    del self.channels[key][num]
                else:
                    num += 1
        else:
            del self.channels[key]
