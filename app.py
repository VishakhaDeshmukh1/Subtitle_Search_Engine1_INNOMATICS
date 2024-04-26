import streamlit as st
import chromadb
import time
import ast

# load the dataset
path = "C:\\Users\\visha\\Downloads\\Subtitle_Seachengine\\Subtitle_Search_Engine-main\\Subtitle_Search_Engine-main\\db"

client = chromadb.PersistentClient(path=path)
client.heartbeat()
collection = client.get_collection(name="subtitle_sem")

def similar_title(query_text):

    result = collection.query(
        query_texts=query_text,
        include=["metadatas", "distances"],
        n_results=5
    )
    ids = result['ids'][0]
    distances = result['distances'][0]
    metadatas = result['metadatas'][0]

    # convert the metadatas list to a list of dictionaries
    metadatas = [ast.literal_eval(metadata) for metadata in metadatas]

    zipped_data = zip(metadatas, ids, distances)
    sorted_data = sorted(zipped_data, key=lambda x: x[2], reverse=True)
    return sorted_data

st.title("🔍Subtitle Search: Your Gateway to Quality Content Discovery 🎬")
st.subheader("🔍 Shortcut to Content Discovery 🚀")

query_text = st.text_input('Enter your search query:')
search = st.button("Search")
if search:  
    result = collection.query(
        query_texts = query_text,
        include=["metadatas", 'distances'],
        n_results=10
    )

    with st.spinner('Wait for it...'):
        time.sleep(5)

    st.success('Here are the most relevant 10 subtitle names:')
    ids = result['ids'][0]
    distances = result['distances'][0]
    metadatas = result['metadatas'][0]
    zipped_data = zip(metadatas, ids, distances)
    sorted_data = sorted(zipped_data, key=lambda x: x[2], reverse=True)

    for metadata, ids, distance in sorted_data:
        subtitle_name = metadata['subtitle_name']
        subtitle_id = metadata['subtitle_id']
        subtitle_link = f"https://www.opensubtitles.org/en/subtitles/{subtitle_id}"
        st.markdown(f"[{subtitle_name}]({subtitle_link})")






