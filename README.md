## Requirements
![](https://img.shields.io/badge/python-3.10-green.svg)
----
# Installation
[Highly recommended] create a new conda environment
Conda

If you are using conda, you can follow this step
~~~
conda create --name llama python=3.10
~~~
And activate the environmetn
~~~
conda activate llama
~~~

# Streamlit Application Readme

This readme provides instructions on how to use the Streamlit application titled `new_llama.py`. Additionally, it guides you on how to customize Pinecone API credentials by modifying the `secrets.toml` file within the `.streamlit` folder. For a visual demonstration of the application, refer to the included video located at `video/demo.mkv`.

## Getting Started

To run the Streamlit application, follow these steps:

1. Open a terminal window.

2. Navigate to the directory containing the `new_llama.py` file.

3. Run the following command to start the Streamlit application:

    ```bash
    streamlit run new_llama.py
    ```

4. Once the application is launched, open a web browser and go to the provided URL (usually `http://localhost:8501`).

5. Explore the features and functionalities of the Streamlit application through the user interface.

## Customizing Pinecone API Credentials

If you wish to use your own Pinecone account and replicate API credentials, follow these steps:

1. Locate the `.streamlit` folder within the project directory.

2. Open the `secrets.toml` file within the `.streamlit` folder using a text editor of your choice.

3. Update the Pinecone API credentials with your own credentials. This typically includes details such as API key, secret key, and other relevant information.

4. Save the changes to the `secrets.toml` file.

## Video Demo
For a visual walkthrough of the Streamlit application, watch the included demo video. The video provides a comprehensive overview of the application's features and functionalities.
![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)
