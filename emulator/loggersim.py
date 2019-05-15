import logging

log = logging.getLogger('dummy_application')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()

log.addHandler(handler)
