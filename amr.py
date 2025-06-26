import streamlit as st
import pandas as pd
import altair as alt
import time

st.title("Product Analysis App")

start_time = time.time()
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    st.write("File uploaded.")
    load_start = time.time()
    
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write(f"File loaded in {time.time() - load_start:.2f} seconds.")
    st.write("Data Preview:")
    st.dataframe(df.head())

    if df.shape[1] < 27:
        st.warning("The file must have at least 27 columns.")
    else:
        rename_start = time.time()
        df.rename(columns={df.columns[25]: "Sub Products", df.columns[26]: "Products"}, inplace=True)
        st.write(f"Columns renamed in {time.time() - rename_start:.2f} seconds.")

        st.write("Choose a function:")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Product Proportions"):
                process_start = time.time()
                counts = df["Products"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Products": counts.index,
                    "Percentage": percentages.values
                })
                st.write(f"Proportion data prepared in {time.time() - process_start:.2f} seconds.")

                chart_start = time.time()
                pie_chart = alt.Chart(chart_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Products:N",
                    tooltip=["Products", "Percentage"]
                )
                st.write(f"Chart generated in {time.time() - chart_start:.2f} seconds.")
                st.altair_chart(pie_chart, use_container_width=True)

        with col2:
            show_filter = st.session_state.get("show_filter", False)
            if st.button("Filter by Product"):
                st.session_state["show_filter"] = True
                show_filter = True

            if show_filter:
                select_start = time.time()
                selected = st.selectbox("Select a Product", df["Products"].dropna().unique())
                filtered = df[df["Products"] == selected]

                counts = filtered["Sub Products"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Sub Products": counts.index,
                    "Percentage": percentages.values
                })
                st.write(f"Filtered and prepared chart data in {time.time() - select_start:.2f} seconds.")

                chart_start = time.time()
                pie_chart = alt.Chart(chart_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Sub Products:N",
                    tooltip=["Sub Products", "Percentage"]
                )
                st.write(f"Chart generated in {time.time() - chart_start:.2f} seconds.")
                st.altair_chart(pie_chart, use_container_width=True)

st.write(f"Total runtime so far: {time.time() - start_time:.2f} seconds.")
