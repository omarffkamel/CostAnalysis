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

    if df.shape[1] < 28:
        st.warning("The file must have at least 28 columns.")
    else:
        df.rename(columns={
            df.columns[15]: "Cost",           # Column P
            df.columns[25]: "Sub Products",
            df.columns[26]: "Products",
            df.columns[27]: "Product ID"
        }, inplace=True)

        st.write("Choose a function:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Product Proportions"):
                counts = df["Products"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Products": counts.index,
                    "Percentage": percentages.values
                })
                pie_chart = alt.Chart(chart_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Products:N",
                    tooltip=["Products", "Percentage"]
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col2:
            show_filter = st.session_state.get("show_filter", False)
            if st.button("Filter by Subproduct"):
                st.session_state["show_filter"] = True
                show_filter = True

            if show_filter:
                selected = st.selectbox("Select a Product", df["Products"].dropna().unique())
                filtered = df[df["Products"] == selected]

                counts = filtered["Sub Products"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Sub Products": counts.index,
                    "Percentage": percentages.values
                })
                pie_chart = alt.Chart(chart_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Sub Products:N",
                    tooltip=["Sub Products", "Percentage"]
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col3:
            show_custom = st.session_state.get("show_custom", False)
            if st.button("Filter by Product I.D"):
                st.session_state["show_custom"] = True
                show_custom = True

            if show_custom:
                selected = st.selectbox("Select a Product (Product ID)", df["Products"].dropna().unique(), key="custom_select")
                filtered = df[df["Products"] == selected]

                counts = filtered["Product ID"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Product ID": counts.index,
                    "Percentage": percentages.values
                })
                pie_chart = alt.Chart(chart_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Product ID:N",
                    tooltip=["Product ID", "Percentage"]
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col4:
            show_cost = st.session_state.get("show_cost", False)
            if st.button("Cost Breakdown by Subproduct"):
                st.session_state["show_cost"] = True
                show_cost = True

            if show_cost:
                selected = st.selectbox("Select a Product (for Cost)", df["Products"].dropna().unique(), key="cost_select")
                filtered = df[df["Products"] == selected]

                cost_df = filtered.groupby("Sub Products")["Cost"].sum().reset_index()
                total_cost = cost_df["Cost"].sum()
                cost_df["Percentage"] = (cost_df["Cost"] / total_cost) * 100

                pie_chart = alt.Chart(cost_df).mark_arc().encode(
                    theta="Percentage:Q",
                    color="Sub Products:N",
                    tooltip=["Sub Products", "Cost", "Percentage"]
                )
                st.altair_chart(pie_chart, use_container_width=True)

st.write(f"Total runtime so far: {time.time() - start_time:.2f} seconds.")
