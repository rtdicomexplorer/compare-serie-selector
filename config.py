# config.py

PACS_AE_TITLE = "MY_AE"
PACS_IP = "10.0.0.1"
PACS_PORT = 104
LOCAL_AE_TITLE = "LOCAL_AE"

MAX_SLICE_THICKNESS = 5.0
PREFERRED_SLICE_THICKNESS = 1.0

KERNEL_EXCLUDE_KEYWORDS = ["lung", "bone", "b60", "b70"]

PHASE_PRIORITY_KEYWORDS = {
    "venous": ["ven", "portal", "pv"],
    "arterial": ["art"],
    "native": ["native", "nativ"]
}

TIME_DELTA_DAYS = 90