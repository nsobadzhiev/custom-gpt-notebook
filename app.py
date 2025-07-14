def main():
    import streamlit.web.bootstrap
    streamlit.web.bootstrap.run("app.py", False, [], flag_options={})  # or use subprocess

if __name__ == "__main__":
    main()
