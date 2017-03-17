class Commands:
    """Static class to hold the commands."""

    @staticmethod
    def extract_key(input_file_path, output_key_file, password):
        """
        Defines extract key command.

        :param input_file_path: Input certificate file.
        :param output_key_file: Key output file.
        :param password: Certificate password.
        :return: List containing command arguments.
        """
        return [
            'openssl',
            'pkcs12',
            '-in',
            input_file_path,
            '-nocerts',
            '-out',
            output_key_file,
            '-passin',
            'pass:' + password,
            '-passout',
            'pass:' + password
        ]

    @staticmethod
    def remove_key_pass(output_key_file, password):
        """
        Command to remove password from private key. Generates separate private key file.

        :param output_key_file: Output key file.
        :param password: Private key password.
        :return: List of command arguments.
        """
        return [
            'openssl',
            'rsa',
            '-in',
            output_key_file,
            '-out',
            output_key_file,
            '-passin',
            'pass:' + password
        ]

    @staticmethod
    def extract_certificate(input_file_path, output_cert_file, password):
        """
        Extracts the actual security certificate.

        :param input_file_path: Source file.
        :param output_cert_file: Certificate output file.
        :param password: Private key password.
        :return: List ot command arguments.
        """

        return [
            'openssl',
            'pkcs12',
            '-in',
            input_file_path,
            '-clcerts',
            '-nokeys',
            '-out',
            output_cert_file,
            '-passin',
            'pass:' + password
        ]
