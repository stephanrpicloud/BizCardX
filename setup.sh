mkdir -p ~/.streamlit/
echo "[server]\nheadless = true\nport = $PORT\nenableCORS = false\n\n" > ~/.streamlit/config.toml
pip install git+https://github.com/victoryhb/streamlit-option-menu.git
