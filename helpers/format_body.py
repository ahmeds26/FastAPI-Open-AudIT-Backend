import urllib.parse


def dict_to_data_binary_string(body: dict, boundary: str):

    payload = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[access_token]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['access_token']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='input_type'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['input_type']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='upload_file'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['upload_file']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='upload_input'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['upload_input']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[attributes][type]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['attributes']['type']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[attributes][name]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['attributes']['name']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[attributes][hostname]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['attributes']['host_name']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[attributes][ip]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['attributes']['ip']}\r\n"
        f"--{boundary}--\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name='data[attributes][subnet]'\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{body['data']['attributes']['subnet']}\r\n"
        f"--{boundary}--\r\n"
    )
    return payload

# Convert nested dict → flat dict with keys like data[attributes][name]
def flatten(prefix: str, obj: dict, result: dict):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}[{k}]" if prefix else k
            flatten(new_prefix, v, result)
    else:
        result[prefix] = obj

def dict_to_encodedurl_string(body: dict):
    body_flat = {}
    flatten("", body, body_flat)
    encoded_string = urllib.parse.urlencode(body_flat)
    return encoded_string