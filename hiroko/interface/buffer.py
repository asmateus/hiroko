'''
    The data of the process can be accessed in real time via the buffer interface.
    This also implements the singleton design pattern
'''
from interface.CSVManager import DATA_PTH
import time


def isBufferOpen(func):
    def check(*args):
        if args[0]._buffer_state is OnlineBuffer.BUFFER_STATE_OPEN:
            func(*args)
        else:
            print('Buffer is closed')
            return
    return check


class OnlineBuffer:
    instance = None
    BUFFER_STATE_CLOSED = 0
    BUFFER_STATE_OPEN = 1

    @staticmethod
    def getInstance():
        if not OnlineBuffer.instance:
            OnlineBuffer.instance = OnlineBuffer()
        return OnlineBuffer.instance

    def __init__(self):
        self._buffer_state = 0
        self._read_lock = False
        self._write_lock = False
        self._buffer = None

    def open(self):
        if self._buffer_state is OnlineBuffer.BUFFER_STATE_CLOSED:
            self._buffer_state = OnlineBuffer.BUFFER_STATE_OPEN
        else:
            print('>>> Buffer is already open')
        self._buffer = list()
        self._buffer.append((-1, [int(time.time())]))

    def close(self, save=False):
        if self._buffer_state is OnlineBuffer.BUFFER_STATE_CLOSED:
            print('>>> Buffer is already closed')
        else:
            self._buffer_state = OnlineBuffer.BUFFER_STATE_CLOSED

        while self._read_lock:
            pass

        if save:
            self._save()
        self._buffer = None
        print('>>> Closed Buffer <online>')

    @isBufferOpen
    def writeBuffer(self, head, content):
        # Wait until buffer becomes available
        while self._read_lock or self._write_lock:
            pass
        self._write_lock = True

        # Check if head already exists
        if head in list(zip(*self._buffer))[0]:
            return
        self._buffer.append((head, content))
        self._write_lock = False

    @isBufferOpen
    def readBuffer(self, head=-1, pretty=False):
        # Wait until buffer becomes available
        while self._read_lock or self._write_lock:
            pass
        self._read_lock = True

        # Read specified head
        if len(self._buffer) is 1:
            return ()
        if head is -1:
            if pretty is False:
                return self._buffer[-1]
            else:
                return self._prettify(self._buffer[-1])

        # Search for head number and return the tuple
        return_val = self._buffer[list(zip(*self._buffer))[0].index(head)]
        if pretty is False:
            return return_val
        else:
            return self._prettify(return_val)

    def _prettify(self, ret_tuple):
        return ret_tuple

    def _save(self):
        save_lst = list()
        for head, content in self._buffer:
            head_str = '*' * 3 + str(head) + '*' * 3
            content_str = '\n'.join([str(c) for c in content])
            save_lst.append(head_str + '\n' + content_str)
        save_str = '\n'.join(save_lst)
        with open(DATA_PTH + str(self._buffer[0][1][0]) + '.dump', 'wb') as ff:
            ff.write(save_str.encode('utf-8'))
