mkdir -p ~/.streamlit/

echo "
[general]
email = "ivo.sonntag@googlemail.com"n
" > ~/.streamlit/credentials.toml

echo "
[server]
headless = true
port = $PORT
enableCORS=false
" > ~/.streamlit/config.toml