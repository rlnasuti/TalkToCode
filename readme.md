# Talk To Code
This is a prototype for talking to your code!

To run it, follow these steps:

1. Populate the following environment variables:
    - OPENAI_API_KEY
2. Run app.py
3. Give the url for an https "git clone" - e.g. "https://github.com/langchain-ai/langchain.git"
4. The app will clone down the repo, index it, and you can start talking to your code!


Note: Depending on the size of the repo, the indexing operation may take some time and your api calls to the embedding point may be throttled. In my testing, this is not a problem. Just wait and eventually the indexing operation will complete.

If you want to reindex a repo, manually delete it out of the dbs directory.