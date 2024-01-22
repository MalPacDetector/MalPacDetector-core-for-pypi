import json

MAX_RECORD_NUMBER = 1000

class Record:
    def __init__(self, file_path: str, start_line: int, start_column: int, end_line: int, end_column: int):
        self.file_path = file_path
        self.content = {
            'start': {
                'line': start_line,
                'column': start_column
            },
            'end': {
                'line': end_line,
                'column': end_column
            }
        }

class PositionRecorder:
    def __init__(self):
        # setup.py
        self.include_ip_in_install_script = []
        self.use_base64_conversion_in_install_script = []
        self.include_base64_string_in_install_script = []
        self.decode_base64_string_in_install_script = []
        self.include_domain_in_install_script = []
        self.include_byte_string_in_install_script = []
        self.use_operating_system_in_install_script = []
        self.use_process_in_install_script = []
        self.use_fs_in_install_script = []
        self.use_network_in_install_script = []
        self.use_env_in_install_script = []
        self.include_suspicious_string_in_install_script = []
        self.use_crypto_and_zip_in_install_script = []
        self.use_eval_in_install_script = []
        self.use_exec_in_install_script = []
        self.use_obfuscation_in_install_script = []
        # python file (except setup.py)
        self.include_ip_in_py_file = []
        self.use_base64_conversion_in_py_file = []
        self.include_base64_string_in_py_file = []
        self.decode_base64_string_in_py_file = []
        self.include_domain_in_py_file = []
        self.include_byte_string_in_py_file = []
        self.use_operating_system_in_py_file = []
        self.use_process_in_py_file = []
        self.use_fs_in_py_file = []
        self.use_network_in_py_file = []
        self.use_env_in_py_file = []
        self.include_suspicious_string_in_py_file = []
        self.use_crypto_and_zip_in_py_file = []
        self.use_eval_in_py_file = []
        self.use_exec_in_py_file = []
        self.use_obfuscation_in_py_file = []

    def add_record(self, feauture_name: str, record: Record) -> None:
        if hasattr(self, feauture_name):
            if len(getattr(self, feauture_name)) >= MAX_RECORD_NUMBER:
                return
            getattr(self, feauture_name).append(record)

    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)