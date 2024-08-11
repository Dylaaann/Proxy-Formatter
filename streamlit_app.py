import streamlit as st

def convert_format(input_str):
    username, password, ip, port = input_str.strip().split(':')

    http_url = f"http://{username}:{password}@{ip}:{port}"
    socks5_url = f"socks5://{username}:{password}@{ip}:{port}"
    auto_url = f"auto://{username}:{password}@{ip}:{port}"

    return http_url, socks5_url, auto_url

def reverse_format(input_str):
    parts = input_str.split("://")
    if len(parts) != 2:
        return input_str, input_str, input_str

    proto, rest = parts
    rest_parts = rest.split('@')
    if len(rest_parts) != 2:
        return input_str, input_str, input_str

    credentials, address = rest_parts
    address_parts = address.split(':')
    if len(address_parts) != 2:
        return input_str, input_str, input_str

    ip, port = address_parts
    username, password = credentials.split(':')

    reversed_http = f"http://{ip}:{port}@{username}:{password}"
    reversed_socks5 = f"socks5://{ip}:{port}@{username}:{password}"
    reversed_auto = f"auto://{ip}:{port}@{username}:{password}"

    return reversed_http, reversed_socks5, reversed_auto

def swap_at_colon(input_str):
    parts = input_str.split("://")
    if len(parts) != 2:
        return input_str, input_str, input_str

    proto, rest = parts
    rest_parts = rest.split('@')
    if len(rest_parts) != 2:
        return input_str, input_str, input_str

    credentials, address = rest_parts
    address_parts = address.split(':')
    if len(address_parts) != 2:
        return input_str, input_str, input_str

    ip, port = address_parts
    username, password = credentials.split(':')

    swapped_http = f"http://{username}:{password}:{ip}:{port}"
    swapped_socks5 = f"socks5://{username}:{password}:{ip}:{port}"
    swapped_auto = f"auto://{username}:{password}:{ip}:{port}"

    return swapped_http, swapped_socks5, swapped_auto

def process_input(input_text, swap=False, swap_colon=False, remove_prefix=False):
    lines = input_text.strip().splitlines()

    http_lines = []
    socks5_lines = []
    auto_lines = []

    for line in lines:
        if line.strip():
            http_url, socks5_url, auto_url = convert_format(line)
            if swap:
                http_url, socks5_url, auto_url = reverse_format(http_url)
            if swap_colon:
                http_url, socks5_url, auto_url = swap_at_colon(http_url)
            if remove_prefix:
                http_url = http_url.split("://")[1]
                socks5_url = socks5_url.split("://")[1]
                auto_url = auto_url.split("://")[1]
            http_lines.append(http_url)
            socks5_lines.append(socks5_url)
            auto_lines.append(auto_url)

    return http_lines, socks5_lines, auto_lines

# Streamlit App
st.title("📄 Proxy Format Converter")
st.write("Paste your proxy credentials below to get converted URLs displayed.")

# Text area for input
input_text = st.text_area("User:Pass:IP:Port", height=200)

# Swap options
swap_option = st.checkbox("Swap IP:Port and Username:Password")
swap_colon_option = st.checkbox("Swap '@' with ':'")

# Option to remove prefixes
remove_prefix = st.checkbox("Remove 'http://', 'socks5://', or 'auto://' prefixes")

if input_text:
    # Process the pasted input text
    http_lines, socks5_lines, auto_lines = process_input(input_text, swap=swap_option, swap_colon=swap_colon_option, remove_prefix=remove_prefix)

    # Combine all the converted proxies into one text
    combined_text = "\n".join(["HTTP Proxies:"] + http_lines + ["\nSocks5 Proxies:"] + socks5_lines + ["\nAuto Proxies:"] + auto_lines)

    # Display the combined output in a single text box
    st.text_area("Converted Proxies", combined_text, height=300)

    # Download button for all proxies
    st.download_button(label="Download All Proxies", data=combined_text, file_name="all_proxies.txt", mime="text/plain")
