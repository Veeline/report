import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import streamlit  as st
import base64


def get_base64_image(imagePath):
    with open(imagePath,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

img_data = get_base64_image("5583046.jpg")


st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img_data}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <h1 style='
        background: linear-gradient(90deg, white, white);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
    '>Scanning VS DPR</h1>
    """,
    unsafe_allow_html=True
)

uid = "vmlitagm"
pwd = "Manish@25"

mpwd="Vil@2024"
sik="Sik@121"
sur="Sur@211"
nal="Nal@122"


current_date = datetime.now().strftime("%Y-%m-%d")



st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #BBDEFB;
        color: blue;
        height: 40px;
        width: 100px;
        font-size: 30px;
        border-radius: 20px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #74C476;
    }
    </style>
""", unsafe_allow_html=True)


scan="http://52.140.78.30:10108/VILUAT_29378/ODataV4/Company('Veeline%20Industries%20Limited')/FinalStageScanning?$filter=Date eq {}" .format(current_date)
#dpr="http://52.140.78.30:10108/VILUAT_29378/ODataV4/Company('Veeline%20Industries%20Limited')/ItemLedgerEntires?$filter=Posting_Date eq {}" .format(current_date)
resp1 = requests.get(scan,auth=HTTPBasicAuth(uid,pwd))
#resp2 = requests.get(dpr,auth=HTTPBasicAuth(uid,pwd))

def report(branch):
    scan="http://52.140.78.30:10108/VILUAT_29378/ODataV4/Company('Veeline%20Industries%20Limited')/FinalStageScanning?$filter=Date eq {}" .format(current_date)
    dpr="http://52.140.78.30:10108/VILUAT_29378/ODataV4/Company('Veeline%20Industries%20Limited')/ItemLedgerEntires?$filter=Posting_Date eq {}" .format(current_date)
    resp1 = requests.get(scan,auth=HTTPBasicAuth(uid,pwd))
    resp2 = requests.get(dpr,auth=HTTPBasicAuth(uid,pwd))
    data = resp1.json()["value"]
    data2 = resp2.json()["value"]
    scandf=pd.DataFrame(data)
    dprdf=pd.DataFrame(data2)
    if branch and not scandf.empty and not dprdf.empty:
        scandf = scandf[scandf["Branch"] == branch][["Line_No","Date","Branch","Division"]]
        dprdf=dprdf[(dprdf["Entry_Type"].str.startswith("Output")) & (dprdf["Source_No"].str.startswith("FG")) & (dprdf["Global_Dimension_1_Code"]==branch)][["Posting_Date","Global_Dimension_1_Code","Global_Dimension_2_Code","Quantity"]]
        dprdf["key"]=dprdf["Posting_Date"].astype(str)+"/"+dprdf["Global_Dimension_1_Code"]+"/"+dprdf["Global_Dimension_2_Code"]
        scandf["key"]=scandf["Date"].astype(str)+"/"+scandf["Branch"]+"/"+scandf["Division"] 
        scan_data = scandf.groupby("key")["Line_No"].count()
        output_data = dprdf.groupby("key")["Quantity"].sum()
        result = pd.merge(scan_data,output_data,how="left",on="key")
        result["Quantity"]=result["Quantity"].fillna(0)
        result=result.reset_index()
        result["Date"]=result["key"].str.split("/").apply(lambda x: x[0])
        result["Branch"]=result["key"].str.split("/").apply(lambda x: x[1])
        result["Division"]=result["key"].str.split("/").apply(lambda x: x[2])
        result.rename(columns={"Line_No":"Scan","Quantity":"DPR"},inplace=True)
        result = result[result["Branch"]!=""]
        # Melt the DataFrame to long format
        df_melted = result.melt(
        id_vars=["Branch", "Division", "Date"],
        value_vars=["Scan", "DPR"],
        var_name="Metric",
        value_name="Value"
            )
        # Pivot to reshape with Line_No and Quantity side-by-side for each Date
        pivot = df_melted.pivot_table(
        index=["Branch", "Division"],
        columns=["Date", "Metric"],
        values="Value",
        aggfunc="sum",
        fill_value=0
            )
        # Flatten the multi-level column index (optional but cleaner)
        pivot.columns = [f"{date} {metric}" for date, metric in pivot.columns]
        pivot = pivot.reset_index()
        st.write(pivot)
        st.write(
             "Scanning table: ",scandf.shape , "DPR table: ",dprdf.shape
         )

      
    elif branch==None and not scandf.empty and not dprdf.empty :
        scandf = scandf[["Line_No","Date","Branch","Division"]]
        dprdf=dprdf[(dprdf["Entry_Type"].str.startswith("Output")) & (dprdf["Source_No"].str.startswith("FG"))][["Posting_Date","Global_Dimension_1_Code","Global_Dimension_2_Code","Quantity"]]
        dprdf["key"]=dprdf["Posting_Date"].astype(str)+"/"+dprdf["Global_Dimension_1_Code"]+"/"+dprdf["Global_Dimension_2_Code"]
        scandf["key"]=scandf["Date"].astype(str)+"/"+scandf["Branch"]+"/"+scandf["Division"] 
        scan_data = scandf.groupby("key")["Line_No"].count()
        output_data = dprdf.groupby("key")["Quantity"].sum()
        result = pd.merge(scan_data,output_data,how="left",on="key")
        result["Quantity"]=result["Quantity"].fillna(0)
        result=result.reset_index()
        result["Date"]=result["key"].str.split("/").apply(lambda x: x[0])
        result["Branch"]=result["key"].str.split("/").apply(lambda x: x[1])
        result["Division"]=result["key"].str.split("/").apply(lambda x: x[2])
        result.rename(columns={"Line_No":"Scan","Quantity":"DPR"},inplace=True)
        result = result[result["Branch"]!=""]
        # Melt the DataFrame to long format
        df_melted = result.melt(
        id_vars=["Branch", "Division", "Date"],
        value_vars=["Scan", "DPR"],
        var_name="Metric",
        value_name="Value"
            )
        # Pivot to reshape with Line_No and Quantity side-by-side for each Date
        pivot = df_melted.pivot_table(
        index=["Branch", "Division"],
        columns=["Date", "Metric"],
        values="Value",
        aggfunc="sum",
        fill_value=0
            )
        # Flatten the multi-level column index (optional but cleaner)
        pivot.columns = [f"{date} {metric}" for date, metric in pivot.columns]
        pivot = pivot.reset_index()
        st.write(pivot)
        st.write(
             "Scanning table: ",scandf.shape , "DPR table: ",dprdf.shape
         )
    else:
         st.write( "Unavailability of data Scanning table: ",scandf.shape , "DPR table: ",dprdf.shape
         )

if resp1.status_code==200 : 
    st.write("Online")
    access=st.text_input("Enter the access password",type="password")
    if access==mpwd:
        if st.button("Refresh"):
            report(branch=None)
    elif access==sik:
        if st.button("Refresh"):
            report(branch="SIK")
    elif access==sur:
        if st.button("Refresh"):
            report(branch="SUR")
    elif access==nal:
        if st.button("Refresh"):
            report(branch="NAL")
    else:
        st.write("Enter a valid passkey")
                    
else:
    st.write("DataBase authentication error:")    
         