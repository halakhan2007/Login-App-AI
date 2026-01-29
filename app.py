import streamlit as st
import pandas as pd
import os
# --------------------------PAGE CONFIGURATION----------------------------
st.set_page_config(page_title="Smart AI Healthcare System", layout="centered")
st.title("🏥 Smart AI Healthcare System")
st.subheader("Secure Patient Access & AI Disease Prediction")
st.markdown("---")

#------------------------------LOAD DATABASE----------------------------------
DATA_FILE="Patients.csv"
if os.path.exists(DATA_FILE):
    df=pd.read_csv(DATA_FILE)
    #clean data
    df["Patient_ID"]= df["Patient_ID"].astype(str).str.strip()
    df["Name"]=df["Name"].astype(str).str.strip().str.lower()
    df["DOB"]=df["DOB"].astype(str).str.strip()
else:
    df=pd.DataFrame(columns=["Patient_ID", "Name", "DOB"])
    df.to_csv(DATA_FILE, index=False)

#---------------------------------SESSION STATE------------------------------------
if "attempts" not in st.session_state:
    st.session_state.attempts=0
if "authenticated" not in st.session_state:
    st.session_state.authenticated= False
if "current_patient" not in st.session_state:
    st.session_state.current_patient=None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
    
#------------------------------LOGIN SECTION----------------------------------------
st.header("🔐 Patient Login")

patient_id = st.text_input("Enter Patient ID")

if patient_id:

    if patient_id in df["Patient_ID"].values:
        name = st.text_input("Enter Full Name")
        dob = st.text_input("Enter Date of Birth (DD-MM-YYYY)")

        if st.button("Verify Identity"):
            record = df[df["Patient_ID"] == patient_id].iloc[0]

            input_name = name.strip().lower()
            input_dob = dob.strip()
            stored_name = record["Name"]
            stored_dob = record["DOB"]
            if input_name == stored_name and input_dob == stored_dob:
                st.success("✅ Identity Verified. Access Granted.")
                st.session_state.authenticated = True
                st.session_state.attempts = 0
                st.session_state.current_patient = patient_id
            else:
                st.session_state.attempts += 1
                remaining = 3 - st.session_state.attempts

                if remaining <= 0:
                    st.error("🚨 Access Blocked due to multiple failed attempts")
                else:
                    st.warning(f"❌ Incorrect details. Attempts left: {remaining}")

    else:
        st.error("❌ Patient ID not registered")
        st.info("Please register to continue.")

        st.markdown("📝 New Patient Registration")

        new_id = st.text_input("Create Patient ID (e.g. P-1010)")
        new_name = st.text_input("Full Name")
        new_dob = st.text_input("Date of Birth (DD-MM-YYYY)")

        if st.button("Register"):

            if new_id in df["Patient_ID"].values:
                st.error("🚫 Patient ID already exists")
            elif new_id == "" or new_name == "" or new_dob == "":
                st.warning("⚠️ Please fill all fields")
            else:
                new_row = {
                    "Patient_ID": new_id,
                    "Name": new_name,
                    "DOB": new_dob
                }

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

                st.success("🎉 Registration Successful")
                st.info("You can now log in using your Patient ID")
