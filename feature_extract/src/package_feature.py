class PackageFeature:
    def __init__(self):
        # setup.py
        self.include_ip_in_install_script = 'false'
        self.use_base64_conversion_in_install_script = 'false'
        self.include_base64_string_in_install_script = 'false'
        self.decode_base64_string_in_install_script = 'false'
        self.include_domain_in_install_script = 'false'
        self.include_byte_string_in_install_script = 'false'
        self.use_operating_system_in_install_script = 'false'
        self.use_process_in_install_script = 'false'
        self.use_fs_in_install_script = 'false'
        self.use_network_in_install_script = 'false'
        self.use_env_in_install_script = 'false'
        self.include_suspicious_string_in_install_script = 'false'
        self.use_crypto_and_zip_in_install_script = 'false'
        self.use_eval_in_install_script = 'false'
        self.use_exec_in_install_script = 'false'
        self.use_obfuscation_in_install_script = 'false'
        # python file (except setup.py)
        self.include_ip_in_py_file = 'false'
        self.use_base64_conversion_in_py_file = 'false'
        self.include_base64_string_in_py_file = 'false'
        self.decode_base64_string_in_py_file = 'false'
        self.include_domain_in_py_file = 'false'
        self.include_byte_string_in_py_file = 'false'
        self.use_operating_system_in_py_file = 'false'
        self.use_process_in_py_file = 'false'
        self.use_fs_in_py_file = 'false'
        self.use_network_in_py_file = 'false'
        self.use_env_in_py_file = 'false'
        self.include_suspicious_string_in_py_file = 'false'
        self.use_crypto_and_zip_in_py_file = 'false'
        self.use_eval_in_py_file = 'false'
        self.use_exec_in_py_file = 'false'
        self.use_obfuscation_in_py_file = 'false'
        # package metadata
        self.exist_author = 'false'
        self.exist_home_page = 'false'
        self.exist_license = 'false'
        self.is_package_name_in_home_page = 'false'
        # statistical features
        self.longest_string_length = 0
        self.entropy = 0
        self.compression_ratio = 0
    
    def merge(self, other: 'PackageFeature') -> 'PackageFeature':
        """Merge two PackageFeature objects.

        Args:
            other: The other PackageFeature object.

        Returns:
            The merged PackageFeature object.
        """
        # setup.py
        if self.include_ip_in_install_script == 'false':
            self.include_ip_in_install_script = other.include_ip_in_install_script
        if self.use_base64_conversion_in_install_script == 'false':
            self.use_base64_conversion_in_install_script = other.use_base64_conversion_in_install_script
        if self.include_base64_string_in_install_script == 'false':
            self.include_base64_string_in_install_script = other.include_base64_string_in_install_script
        if self.decode_base64_string_in_install_script == 'false':
            self.decode_base64_string_in_install_script = other.decode_base64_string_in_install_script
        if self.include_domain_in_install_script == 'false':
            self.include_domain_in_install_script = other.include_domain_in_install_script
        if self.include_byte_string_in_install_script == 'false':
            self.include_byte_string_in_install_script = other.include_byte_string_in_install_script
        if self.use_process_in_install_script == 'false':
            self.use_process_in_install_script = other.use_process_in_install_script
        if self.use_fs_in_install_script == 'false':
            self.use_fs_in_install_script = other.use_fs_in_install_script
        if self.use_network_in_install_script == 'false':
            self.use_network_in_install_script = other.use_network_in_install_script
        if self.use_env_in_install_script == 'false':
            self.use_env_in_install_script = other.use_env_in_install_script
        if self.include_suspicious_string_in_install_script == 'false':
            self.include_suspicious_string_in_install_script = other.include_suspicious_string_in_install_script
        if self.use_crypto_and_zip_in_install_script == 'false':
            self.use_crypto_and_zip_in_install_script = other.use_crypto_and_zip_in_install_script
        if self.use_eval_in_install_script == 'false':
            self.use_eval_in_install_script = other.use_eval_in_install_script
        if self.use_exec_in_install_script == 'false':
            self.use_exec_in_install_script = other.use_exec_in_install_script
        if self.use_obfuscation_in_install_script == 'false':
            self.use_obfuscation_in_install_script = other.use_obfuscation_in_install_script
        # python file (except setup.py)
        if self.include_ip_in_py_file == 'false':
            self.include_ip_in_py_file = other.include_ip_in_py_file
        if self.use_base64_conversion_in_py_file == 'false':
            self.use_base64_conversion_in_py_file = other.use_base64_conversion_in_py_file
        if self.include_base64_string_in_py_file == 'false':
            self.include_base64_string_in_py_file = other.include_base64_string_in_py_file
        if self.decode_base64_string_in_py_file == 'false':
            self.decode_base64_string_in_py_file = other.decode_base64_string_in_py_file
        if self.include_domain_in_py_file == 'false':
            self.include_domain_in_py_file = other.include_domain_in_py_file
        if self.include_byte_string_in_py_file == 'false':
            self.include_byte_string_in_py_file = other.include_byte_string_in_py_file
        if self.use_process_in_py_file == 'false':
            self.use_process_in_py_file = other.use_process_in_py_file
        if self.use_fs_in_py_file == 'false':
            self.use_fs_in_py_file = other.use_fs_in_py_file
        if self.use_network_in_py_file == 'false':
            self.use_network_in_py_file = other.use_network_in_py_file
        if self.use_env_in_py_file == 'false':
            self.use_env_in_py_file = other.use_env_in_py_file
        if self.include_suspicious_string_in_py_file == 'false':
            self.include_suspicious_string_in_py_file = other.include_suspicious_string_in_py_file
        if self.use_crypto_and_zip_in_py_file == 'false':
            self.use_crypto_and_zip_in_py_file = other.use_crypto_and_zip_in_py_file
        if self.use_eval_in_py_file == 'false':
            self.use_eval_in_py_file = other.use_eval_in_py_file
        if self.use_exec_in_py_file == 'false':
            self.use_exec_in_py_file = other.use_exec_in_py_file
        if self.use_obfuscation_in_py_file == 'false':
            self.use_obfuscation_in_py_file = other.use_obfuscation_in_py_file
        # package metadata
        if self.exist_author == 'false':
            self.exist_author = other.exist_author
        if self.exist_home_page == 'false':
            self.exist_home_page = other.exist_home_page
        if self.exist_license == 'false':
            self.exist_license = other.exist_license
        if self.is_package_name_in_home_page == 'false':
            self.is_package_name_in_home_page = other.is_package_name_in_home_page
        # statistical features
        if self.entropy < other.entropy:
            self.entropy = other.entropy
        if self.compression_ratio < other.compression_ratio:
            self.compression_ratio = other.compression_ratio
        if self.longest_string_length < other.longest_string_length:
            self.longest_string_length = other.longest_string_length