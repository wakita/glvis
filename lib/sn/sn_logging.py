import logging

_log_on_shader_variables = False
_log_on_uniform_update = False


def log_on_shader_variables(b=None):
    global _log_on_shader_variables
    if b is None:
        return _log_on_shader_variables
    else:
        _log_on_shader_variables = b


def log_on_uniform_update(b=None):
    global _log_on_uniform_update
    if b is None:
        return _log_on_uniform_update
    else:
        _log_on_uniform_update = b

log_on_shader_variables(True)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
