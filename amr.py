import streamlit as st
import pandas as pd
import altair as alt
import time

# ✅ Force Altair to use SVG rendering for better fullscreen compatibility
alt.renderers.set_embed_options(renderer="svg")

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
            df.columns[15]: "Cost",
            df.columns[25]: "Sub Products",
            df.columns[26]: "Products",
            df.columns[27]: "Product ID"
        }, inplace=True)

        for key in ["show_filter", "show_custom", "show_cost"]:
            if key not in st.session_state:
                st.session_state[key] = False

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
                pie_chart = alt.Chart(chart_df).mark_arc(tooltip=True).encode(
                    theta="Percentage:Q",
                    color="Products:N"
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col2:
            if st.button("Filter by Subproduct"):
                st.session_state["show_filter"] = True

            if st.session_state["show_filter"]:
                selected = st.selectbox("Select a Product", df["Products"].dropna().unique())
                filtered = df[df["Products"] == selected]

                counts = filtered["Sub Products"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Sub Products": counts.index,
                    "Percentage": percentages.values
                })
                pie_chart = alt.Chart(chart_df).mark_arc(tooltip=True).encode(
                    theta="Percentage:Q",
                    color="Sub Products:N"
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col3:
            if st.button("Filter by Product I.D"):
                st.session_state["show_custom"] = True

            if st.session_state["show_custom"]:
                selected = st.selectbox("Select a Product (Product ID)", df["Products"].dropna().unique(), key="custom_select")
                filtered = df[df["Products"] == selected]

                counts = filtered["Product ID"].value_counts()
                percentages = (counts / counts.sum()) * 100
                chart_df = pd.DataFrame({
                    "Product ID": counts.index,
                    "Percentage": percentages.values
                })
                pie_chart = alt.Chart(chart_df).mark_arc(tooltip=True).encode(
                    theta="Percentage:Q",
                    color="Product ID:N"
                )
                st.altair_chart(pie_chart, use_container_width=True)

        with col4:
            if st.button("Cost Breakdown by Subproduct"):
                st.session_state["show_cost"] = True

            if st.session_state["show_cost"]:
                selected = st.selectbox("Select a Product (for Cost)", df["Products"].dropna().unique(), key="cost_select")
                filtered = df[df["Products"] == selected]

                filtered["Cost"] = pd.to_numeric(filtered["Cost"], errors='coerce')
                filtered = filtered.dropna(subset=["Cost"])

                cost_df = filtered.groupby("Sub Products")["Cost"].sum().reset_index()
                cost_df = cost_df[cost_df["Cost"] > 0]
                total_cost = cost_df["Cost"].sum()

                if total_cost == 0 or cost_df.empty:
                    st.warning("No valid cost data to display for this product.")
                else:
                    cost_df["Percentage"] = (cost_df["Cost"] / total_cost) * 100
                    cost_df = cost_df.sort_values("Cost", ascending=False).head(10)
                    pie_chart = alt.Chart(cost_df).mark_arc(tooltip=True).encode(
                        theta="Percentage:Q",
                        color="Sub Products:N"
                    )
                    st.altair_chart(pie_chart, use_container_width=True)

st.write(f"Total runtime so far: {time.time() - start_time:.2f} seconds.")
