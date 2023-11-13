from Dashboardv6 import *
datasetcount = int(0)

st.set_page_config(
                layout="wide"  
                )
# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Outputs: value
if "tabs" not in st.session_state:
    st.session_state["tabs"] = ["Upload Files", "Generate Dashboard in a new Tab"]
tabs = st.tabs(st.session_state["tabs"])



with tabs[0]:
    uploaded_files = st.file_uploader("Upload JMETER .csv File here", accept_multiple_files=True)
    for file in uploaded_files:
        st.write("filename:", file.name)
        filename = file.name
        df = pd.read_csv(file)
        file.seek(0)
        st.write("Your File Has Been Uploaded")

with tabs[1]:
    if st.button("Generate Dashboard"):
        GenerateReport(df)