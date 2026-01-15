from queue import Queue, Full, Empty

# In-memory FIFO queue (edge buffer)
_message_queue = Queue(maxsize=1000)

def enqueue_message(payload: dict):
    """
    Add telemetry to queue (non-blocking).
    """
    try:
        _message_queue.put(payload, block=False)
    except Full:
        # Drop oldest if queue is full
        try:
            _message_queue.get(block=False)
            _message_queue.put(payload, block=False)
        except Empty:
            pass

def dequeue_message():
    """
    Get next telemetry message.
    """
    try:
        return _message_queue.get(block=False)
    except Empty:
        return None
