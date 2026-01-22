"""
Critical Circular Buffer (5-Second Retention)
PDF Phase 3 – Edge Reliability
"""

from collections import deque
import time

# --------------------------------
# Configuration
# --------------------------------

RETENTION_SECONDS = 5
RETENTION_MS = RETENTION_SECONDS * 1000  # 5 seconds

# Optional safety cap (memory protection)
MAX_BUFFER_SIZE = 5000

# --------------------------------
# Circular Buffer Class
# --------------------------------

class CriticalBuffer:
    def __init__(self):
        self.buffer = deque(maxlen=MAX_BUFFER_SIZE)

    def add_event(self, device_id, sensor, value, severity, reason):
        """
        Add a critical/error event
        """
        event = {
            "timestamp": int(time.time() * 1000),
            "device_id": device_id,
            "sensor": sensor,
            "value": round(value, 2),
            "severity": severity,
            "reason": reason
        }

        self.buffer.append(event)
        self._cleanup_old_events()

    def _cleanup_old_events(self):
        """
        Remove events older than 5 seconds
        """
        cutoff_time = int(time.time() * 1000) - RETENTION_MS

        while self.buffer and self.buffer[0]["timestamp"] < cutoff_time:
            self.buffer.popleft()

    def get_all_events(self):
        """
        Return all valid (last 5 seconds) events
        """
        self._cleanup_old_events()
        return list(self.buffer)

    def get_latest_event(self):
        """
        Get most recent critical event
        """
        if not self.buffer:
            return None
        return self.buffer[-1]

    def clear(self):
        """
        Clear entire buffer
        """
        self.buffer.clear()

    def size(self):
        """
        Number of events in buffer
        """
        self._cleanup_old_events()
        return len(self.buffer)

# --------------------------------
# Global Instance (USED BY FAULT DETECTOR)
# --------------------------------

critical_buffer = CriticalBuffer()
