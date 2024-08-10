import streamlit as st

def convert_format(input_str):
    username, password, ip, port = input_str.strip().split(':')

    http_url = f"http://{username}:{password}@{ip}:{port}"
    socks5_url = f"socks5://{username}:{password}@{ip}:{port}"
    auto_url = f"auto://{username}:{password}@{ip}:{port}"

    return http_url, socks5_url, auto_url

def process_file(file_content):
    lines = file_content.strip().splitlines()

    http_lines = []
    socks5_lines = []
    auto_lines = []

    for line in lines:
        if line.strip():
            http_url, socks5_url, auto_url = convert_format(line)
            http_lines.append(http_url)
            socks5_lines.append(socks5_url)
            auto_lines.append(auto_url)

    return http_lines, socks5_lines, auto_lines

# Streamlit App
st.title("📄 Proxy Format Converter")
st.write("Upload a .txt file with proxy credentials to get converted URLs displayed below.")

# File uploader
uploaded_file = st.file_uploader("User:Pass:IP:Port", type="txt")

if uploaded_file:
    # Read and process the uploaded file
    file_content = uploaded_file.read().decode("utf-8")
    http_lines, socks5_lines, auto_lines = process_file(file_content)

    # Display the converted URLs
    st.subheader("HTTP Proxies")
    st.write("\n".join(http_lines))

    st.subheader("Socks5 Proxies")
    st.write("\n".join(socks5_lines))

    st.subheader("Auto Proxies")
    st.write("\n".join(auto_lines))

    # Combine all the converted proxies into one text
    combined_text = "\n".join(["HTTP Proxies:"] + http_lines + ["\nSocks5 Proxies:"] + socks5_lines + ["\nAuto Proxies:"] + auto_lines)

    # Download button for all proxies
    st.download_button(label="Download All Proxies", data=combined_text, file_name="all_proxies.txt", mime="text/plain")
