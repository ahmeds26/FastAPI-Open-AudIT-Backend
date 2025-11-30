import subprocess


def generate_secret_key():

    secret_key = subprocess.run(["openssl", "rand", "-hex", "32"], capture_output=True)
    return secret_key.stdout.decode().strip()
