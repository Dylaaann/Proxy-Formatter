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

# Calculate the height for the text areas based on the number of lines
def calculate_text_area_height(lines):
    base_height = 30  # Base height to accommodate a small amount of text
    line_height = 18  # Approximate height of a single line of text
    return base_height + len(lines) * line_height

# Streamlit App
st.title("📄 Proxy Format Converter")
st.write("Upload a .txt file with proxy credentials to get converted URLs displayed below.")

# File uploader
uploaded_file = st.file_uploader("User:Pass:IP:Port", type="txt")

if uploaded_file:
    # Read and process the uploaded file
    file_content = uploaded_file.read().decode("utf-8")
    http_lines, socks5_lines, auto_lines = process_file(file_content)

    # Display the converted URLs with dynamically adjusted text boxes
    st.subheader("HTTP Proxies")
    http_text = "\n".join(http_lines)
    st.text_area("", http_text, height=calculate_text_area_height(http_lines), key="http_proxies")

    st.subheader("Socks5 Proxies")
    socks5_text = "\n".join(socks5_lines)
    st.text_area("", socks5_text, height=calculate_text_area_height(socks5_lines), key="socks5_proxies")

    st.subheader("Auto Proxies")
    auto_text = "\n".join(auto_lines)
    st.text_area("", auto_text, height=calculate_text_area_height(auto_lines), key="auto_proxies")

    # Combine all the converted proxies into one text
    combined_text = "\n".join(["HTTP Proxies:"] + http_lines + ["\nSocks5 Proxies:"] + socks5_lines + ["\nAuto Proxies:"] + auto_lines)

    # Download button for all proxies
    st.download_button(label="Download All Proxies", data=combined_text, file_name="all_proxies.txt", mime="text/plain")
