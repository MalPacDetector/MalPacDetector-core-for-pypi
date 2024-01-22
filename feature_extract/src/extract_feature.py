import os
import csv

from pkginfo import UnpackedSDist

from .ast_util import get_feature_by_file_path
from .package_feature import PackageFeature
from .statistical_util import calculate_entropy_from_file, calculate_compression_ratio_from_file
from .position_recorder import PositionRecorder


def extract_feature_from_package(package_path: str, feature_file_name: str, feature_file_dir: str, feature_position_file_dir: str)->str:
    """Extract features from a package.
    
    Args:
        package_path: The path of the package.
        feature_file_name: The name of the feature file and the feature position file.
        feature_file_dir: The directory to save the feature file.
        feature_position_file_dir: The directory to save the feature position file.

    Returns:
        The path of the feature file.
    """
    # 1. get all file paths in the package
    file_paths = []
    setup_path = None
    for root, dirs, file_names in os.walk(package_path):
        for file_name in file_names:
            if file_name.endswith('.py'):
                file_paths.append(os.path.join(root, file_name))
        if setup_path is None and 'setup.py' in file_names:
            setup_path = os.path.join(root, 'setup.py')
    # 2. extract features from each file
    package_feature = PackageFeature()
    position_recorder = PositionRecorder()
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        try:
            package_feature_temp = get_feature_by_file_path(file_path, file_name == 'setup.py', position_recorder)
            package_feature.merge(package_feature_temp)
        except Exception:
            pass
    # 3. extract package metadata
    try:
        package_metadata = UnpackedSDist(package_path)
        if package_metadata.author is not None:
            package_feature.exist_author = 'true'
        if package_metadata.home_page is not None:
            package_feature.exist_home_page = 'true'
            if package_metadata.name in package_metadata.home_page:
                package_feature.is_package_name_in_home_page = 'true'
        if package_metadata.license is not None and package_metadata.license.lower() != 'unlicense':
            package_feature.exist_license = 'true'
    except Exception:
        pass
    # 4. extract statistical features
    if setup_path:
        package_feature.entropy = calculate_entropy_from_file(setup_path)
        package_feature.compression_ratio = calculate_compression_ratio_from_file(setup_path)
    # 5. save the features
    dest_path = os.path.join(feature_file_dir, feature_file_name + '.csv')
    with open(dest_path, 'w') as f:
        writer = csv.writer(f)
        # setup.py
        writer.writerow(['include_ip_in_install_script', package_feature.include_ip_in_install_script])
        writer.writerow(['use_base64_conversion_in_install_script', package_feature.use_base64_conversion_in_install_script])
        writer.writerow(['include_base64_string_in_install_script', package_feature.include_base64_string_in_install_script])
        writer.writerow(['decode_base64_string_in_install_script', package_feature.decode_base64_string_in_install_script])
        writer.writerow(['include_domain_in_install_script', package_feature.include_domain_in_install_script])
        writer.writerow(['include_byte_string_in_install_script', package_feature.include_byte_string_in_install_script])
        writer.writerow(['use_process_in_install_script', package_feature.use_process_in_install_script])
        writer.writerow(['use_fs_in_install_script', package_feature.use_fs_in_install_script])
        writer.writerow(['use_network_in_install_script', package_feature.use_network_in_install_script])
        writer.writerow(['use_env_in_install_script', package_feature.use_env_in_install_script])
        writer.writerow(['include_suspicious_string_in_install_script', package_feature.include_suspicious_string_in_install_script])
        writer.writerow(['use_crypto_and_zip_in_install_script', package_feature.use_crypto_and_zip_in_install_script])
        writer.writerow(['use_eval_in_install_script', package_feature.use_eval_in_install_script])
        writer.writerow(['use_exec_in_install_script', package_feature.use_exec_in_install_script])
        writer.writerow(['use_obfuscation_in_install_script', package_feature.use_obfuscation_in_install_script])
        # python file (except setup.py)
        writer.writerow(['include_ip_in_py_file', package_feature.include_ip_in_py_file])
        writer.writerow(['use_base64_conversion_in_py_file', package_feature.use_base64_conversion_in_py_file])
        writer.writerow(['include_base64_string_in_py_file', package_feature.include_base64_string_in_py_file])
        writer.writerow(['decode_base64_string_in_py_file', package_feature.decode_base64_string_in_py_file])
        writer.writerow(['include_domain_in_py_file', package_feature.include_domain_in_py_file])
        writer.writerow(['include_byte_string_in_py_file', package_feature.include_byte_string_in_py_file])
        writer.writerow(['use_process_in_py_file', package_feature.use_process_in_py_file])
        writer.writerow(['use_fs_in_py_file', package_feature.use_fs_in_py_file])
        writer.writerow(['use_network_in_py_file', package_feature.use_network_in_py_file])
        writer.writerow(['use_env_in_py_file', package_feature.use_env_in_py_file])
        writer.writerow(['use_crypto_and_zip_in_py_file', package_feature.use_crypto_and_zip_in_py_file])
        writer.writerow(['use_eval_in_py_file', package_feature.use_eval_in_py_file])
        writer.writerow(['use_exec_in_py_file', package_feature.use_exec_in_py_file])
        writer.writerow(['use_obfuscation_in_py_file', package_feature.use_obfuscation_in_py_file])
        # package metadata
        writer.writerow(['exist_author', package_feature.exist_author])
        writer.writerow(['exist_home_page', package_feature.exist_home_page])
        writer.writerow(['exist_license', package_feature.exist_license])
        writer.writerow(['is_package_name_in_home_page', package_feature.is_package_name_in_home_page])
        # statistical features
        writer.writerow(['entropy', package_feature.entropy])
        writer.writerow(['compression_ratio', package_feature.compression_ratio])
        writer.writerow(['include_suspicious_string_in_py_file', package_feature.include_suspicious_string_in_py_file])
    # 6. save the feature positions
    dest_path = os.path.join(feature_position_file_dir, feature_file_name + '.json')
    with open(dest_path, 'w') as f:
        f.write(position_recorder.serialize())
    return dest_path