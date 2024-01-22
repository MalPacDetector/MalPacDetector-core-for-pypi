import ast
import re
import base64

from .package_feature import PackageFeature
from .patterns import IP_PATTERN, BASE64_PATTERN, SENSITIVE_STRING_PATTERN, DOMAIN_PATTERN
from .position_recorder import Record, PositionRecorder


def get_ast_tree_by_file_path(filename: str):
    """Get the ast tree of a python file.
    
    Args:
        filename: The path of the python file.
        position_recorder: The position recorder.

    Returns:
        The ast tree of the python file.
    """
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    return tree

def get_ast_tree_by_content(content: str):
    """Get the ast tree of a python code.
    
    Args:
        content: The python code.

    Returns:
        The ast tree of the python code.
    """
    tree = ast.parse(content)
    return tree

def get_feature_by_file_path(file_path: str, is_in_setup_py: bool=False, position_recorder: PositionRecorder=None) -> PackageFeature:
    """Get the feature of a python file.

    Args:
        filename: The path of the python file.
        is_in_setup_py: Whether the file is in setup.py.
        position_recorder: The position recorder.

    Returns:
        The feature of the python file.
    """
    tree = get_ast_tree_by_file_path(file_path)
    return get_feature_by_ast(tree, is_in_setup_py, position_recorder, file_path)

def get_feature_by_content(content: str, is_in_setup_py: bool=False, position_recorder: PositionRecorder=None, file_path: str='') -> PackageFeature:
    """Get the feature of a python code.

    Args:
        content: The python code.
        is_in_setup_py: Whether the file is in setup.py.
        position_recorder: The position recorder.
        file_path: The path of the python code file.

    Returns:
        The feature of the python code.
    """
    tree = get_ast_tree_by_content(content)
    return get_feature_by_ast(tree, is_in_setup_py, position_recorder, file_path)

def get_feature_by_ast(tree, is_in_setup_py: bool=False, position_recorder: PositionRecorder=None, file_path: str='') -> PackageFeature:
    """Get the feature of a python ast tree.

    Args:
        tree: The ast tree of the python code.
        is_in_setup_py: Whether the file is in setup.py.
        position_recorder: The position recorder.

    Returns:
        The feature of the python code.
    """
    package_feature = PackageFeature()
    for node in ast.walk(tree):
        t = type(node).__name__
        if t == 'Import':
            for alias in node.names:
                dot_index = alias.name.find('.')
                if dot_index != -1:
                    module_name = alias.name[:dot_index]
                else:
                    module_name = alias.name
                if module_name == 'base64':
                    if is_in_setup_py:
                        package_feature.use_base64_conversion_in_install_script = 'true'
                        position_recorder.add_record('use_base64_conversion_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_base64_conversion_in_py_file = 'true'
                        position_recorder.add_record('use_base64_conversion_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif module_name == 'os' or module_name == 'shutil' or module_name == 'tempfile' or module_name == 'glob' or module_name == 'pathlib':
                    if is_in_setup_py:
                        package_feature.use_fs_in_install_script = 'true'
                        position_recorder.add_record('use_fs_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_fs_in_py_file = 'true'
                        position_recorder.add_record('use_fs_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif module_name == 'subprocess':
                    if is_in_setup_py:
                        package_feature.use_process_in_install_script = 'true'
                        position_recorder.add_record('use_process_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_process_in_py_file = 'true'
                        position_recorder.add_record('use_process_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif module_name == 'httplib' or module_name == 'urllib' or module_name == 'urllib2' or alias.name == 'http.client' or module_name == 'socket' or module_name == 'requests' or module_name == 'aiohttp' or module_name == 'selenium':
                    if is_in_setup_py:
                        package_feature.use_network_in_install_script = 'true'
                        position_recorder.add_record('use_network_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_network_in_py_file = 'true'
                        position_recorder.add_record('use_network_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif alias.name == 'dns.resolver':
                    if is_in_setup_py:
                        package_feature.include_domain_in_install_script = 'true'
                        position_recorder.add_record('include_domain_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.include_domain_in_py_file = 'true'
                        position_recorder.add_record('include_domain_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif module_name == 'zlib' or module_name == 'gzip' or module_name == 'bz2' or module_name == 'tarfile':
                    if is_in_setup_py:
                        package_feature.use_crypto_and_zip_in_install_script = 'true'
                        position_recorder.add_record('use_crypto_and_zip_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_crypto_and_zip_in_py_file = 'true'
                        position_recorder.add_record('use_crypto_and_zip_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
        elif t == 'ImportFrom':
            if node.module == None:
                continue
            dot_index = node.module.find('.')
            if dot_index != -1:
                module_name = node.module[:dot_index]
            else:
                module_name = node.module
            if module_name == 'base64':
                if is_in_setup_py:
                    package_feature.use_base64_conversion_in_install_script = 'true'
                    position_recorder.add_record('use_base64_conversion_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.use_base64_conversion_in_py_file = 'true'
                    position_recorder.add_record('use_base64_conversion_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif module_name == 'os' or module_name == 'shutil' or module_name == 'tempfile' or module_name == 'glob' or module_name == 'pathlib':
                if is_in_setup_py:
                    package_feature.use_fs_in_install_script = 'true'
                    position_recorder.add_record('use_fs_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.use_fs_in_py_file = 'true'
                    position_recorder.add_record('use_fs_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif module_name == 'subprocess':
                if is_in_setup_py:
                    package_feature.use_process_in_install_script = 'true'
                    position_recorder.add_record('use_process_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.use_process_in_py_file = 'true'
                    position_recorder.add_record('use_process_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif module_name == 'httplib' or module_name == 'urllib' or module_name == 'urllib2' or (node.module == 'http' and 'client' in node.names) or module_name == 'socket' or module_name == 'requests' or module_name == 'aiohttp' or module_name == 'selenium':
                if is_in_setup_py:
                    package_feature.use_network_in_install_script = 'true'
                    position_recorder.add_record('use_network_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.use_network_in_py_file = 'true'
                    position_recorder.add_record('use_network_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif node.module == 'dns' and 'resolver' in node.names:
                if is_in_setup_py:
                    package_feature.include_domain_in_install_script = 'true'
                    position_recorder.add_record('include_domain_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.include_domain_in_py_file = 'true'
                    position_recorder.add_record('include_domain_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif module_name == 'zlib' or module_name == 'gzip' or module_name == 'bz2' or module_name == 'tarfile':
                if is_in_setup_py:
                    package_feature.use_crypto_and_zip_in_install_script = 'true'
                    position_recorder.add_record('use_crypto_and_zip_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                else:
                    package_feature.use_crypto_and_zip_in_py_file = 'true'
                    position_recorder.add_record('use_crypto_and_zip_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
        elif t == 'Call':
            if type(node.func).__name__ == 'Name': # open, read, write, eval, exec
                if node.func.id in ['open', 'read', 'write']:
                    if is_in_setup_py:
                        package_feature.use_fs_in_install_script = 'true'
                        position_recorder.add_record('use_fs_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_fs_in_py_file = 'true'
                        position_recorder.add_record('use_fs_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                if node.func.id == 'eval':
                    if is_in_setup_py:
                        package_feature.use_eval_in_install_script = 'true'
                        position_recorder.add_record('use_eval_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_eval_in_py_file = 'true'
                        position_recorder.add_record('use_eval_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif node.func.id == 'exec':
                    if is_in_setup_py:
                        package_feature.use_exec_in_install_script = 'true'
                        position_recorder.add_record('use_exec_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_exec_in_py_file = 'true'
                        position_recorder.add_record('use_exec_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                elif node.func.id == '__pyarmor__':
                    if is_in_setup_py:
                        package_feature.use_obfuscation_in_install_script = 'true'
                        position_recorder.add_record('use_obfuscation_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.use_obfuscation_in_py_file = 'true'
                        position_recorder.add_record('use_obfuscation_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif type(node.func).__name__ == 'Attribute':
                if type(node.func.value).__name__ == 'Name': # os
                    if node.func.value.id == 'os':  # os.system, os.exec*, os.popen, os.spawn*, os.*env
                        if node.func.attr in [
                            'system',
                            'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execvp', 'execvpe',
                            'popen',
                            'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe'
                        ]:
                            if is_in_setup_py:
                                package_feature.use_process_in_install_script = 'true'
                                position_recorder.add_record('use_process_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                            else:
                                package_feature.use_operating_system_in_py_file = 'true'
                                position_recorder.add_record('use_operating_system_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                        elif node.func.attr in [
                            'getenv', 'putenv', 'unsetenv'
                        ]:
                            if is_in_setup_py:
                                package_feature.use_env_in_install_script = 'true'
                                position_recorder.add_record('use_env_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                            else:
                                package_feature.use_env_in_py_file = 'true'
                                position_recorder.add_record('use_env_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    elif node.func.value.id == 'subprocess' and node.func.attr in [
                        'call', 'check_call', 'check_output', 'run', 'getoutput', 'getstatusoutput'
                    ]:
                        if is_in_setup_py:
                            package_feature.use_process_in_install_script = 'true'
                            position_recorder.add_record('use_process_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                        else:
                            package_feature.use_process_in_py_file = 'true'
                            position_recorder.add_record('use_process_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    elif node.func.value.id == 'base64':
                        if node.func.attr == 'b64decode':
                            if is_in_setup_py:
                                package_feature.decode_base64_string_in_install_script = 'true'
                                position_recorder.add_record('decode_base64_string_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                            else:
                                package_feature.decode_base64_string_in_py_file = 'true'
                                position_recorder.add_record('decode_base64_string_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
        elif t == 'Constant':
            if type(node.value).__name__ == 'str':
                if len(node.value) > package_feature.longest_string_length:
                    package_feature.longest_string_length = len(node.value)
                # check if the string contains domain
                if re.search(DOMAIN_PATTERN, node.value):
                    if is_in_setup_py:
                        package_feature.include_domain_in_install_script = 'true'
                        position_recorder.add_record('include_domain_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.include_domain_in_py_file = 'true'
                        position_recorder.add_record('include_domain_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                # check if the string contains base64 string
                if re.search(BASE64_PATTERN, node.value):
                    try:
                        base64_bytes = base64.b64decode(node.value)
                    except:
                        continue

                    if is_in_setup_py:
                        package_feature.include_base64_string_in_install_script = 'true'
                        position_recorder.add_record('include_base64_string_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.include_base64_string_in_py_file = 'true'
                        position_recorder.add_record('include_base64_string_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))

                    try:
                        base64_content = base64_bytes.decode()
                        base64_content_features = get_feature_by_content(base64_content, is_in_setup_py)
                        package_feature.merge(base64_content_features)
                    except:
                        pass
                # check if the string contains ip string
                if re.search(IP_PATTERN, node.value):
                    if is_in_setup_py:
                        package_feature.include_ip_in_install_script = 'true'
                        position_recorder.add_record('include_ip_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.include_ip_in_py_file = 'true'
                        position_recorder.add_record('include_ip_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                # check if the string contains suspicious string
                if re.search(SENSITIVE_STRING_PATTERN, node.value):
                    if is_in_setup_py:
                        package_feature.include_suspicious_string_in_install_script = 'true'
                        position_recorder.add_record('include_suspicious_string_in_install_script', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
                    else:
                        package_feature.include_suspicious_string_in_py_file = 'true'
                        position_recorder.add_record('include_suspicious_string_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
            elif type(node.value).__name__ == 'bytes':
                package_feature.include_byte_string_in_py_file = 'true'
                position_recorder.add_record('include_byte_string_in_py_file', Record(file_path, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset))
    return package_feature
