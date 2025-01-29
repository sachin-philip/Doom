setup(
    name="clayface",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "botter=botter:main",
        ],
    },
    author="Sachin Philip Mathew",
    author_email="me@imsach.in",
    description="Chat interface for Ollama models",
    keywords="chatbot, ollama, streamlit",
    url="http://github.com/labtocat/clayface",  # If you have a repository
)