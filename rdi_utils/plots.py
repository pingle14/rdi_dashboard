import streamlit as st
import altair as alt
import plotly.express as px

# import numpy as np
# import geopandas as gpd


def plot_altair_timeline(df, state_name):
    mini_df = df[df.state_name == state_name]
    nearest = alt.selection(
        type="single", nearest=True, on="mouseover", fields=["Year"], empty="none"
    )

    line = (
        alt.Chart(mini_df)
        .mark_line()
        .encode(
            alt.Y("RDI Index", scale=alt.Scale(zero=False)),
            x="Year",
            color="Type of Percentile:N",
        )
    )
    line.configure_title(align="center")
    selectors = (
        alt.Chart(mini_df)
        .mark_point()
        .encode(x="Year", opacity=alt.value(0))
        .add_selection(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=10, dy=-5).encode(
        text=alt.condition(nearest, "RDI Index", alt.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(mini_df)
        .mark_rule(color="gray")
        .encode(x="Year")
        .transform_filter(nearest)
    )

    chart_title = f"{state_name} RDI Index Over Time"

    # Put pieces of chart together
    chart = alt.layer(line, selectors, points, rules, text).properties(
        title=chart_title
    )

    return chart, chart_title


def plot_timeline(df, state_name):
    fig = px.line(
        df[df.state_name == state_name],
        x="Year",
        y="RDI Index",
        color="Type of Percentile",
        markers=True,
        template="plotly_dark",
    )
    plt_title = f"{state_name} RDI Index Over Time"
    fig.update_layout(
        height=600,
        title_font_size=36,
        title_text=plt_title,
        title_xanchor="center",
        title_x=0.5,
        title_yanchor="top",
        title_y=0.95,
        title_font_color="peachpuff",
        # paper_bgcolor="black",
        # plot_bgcolor="black",
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            # gridwidth=0.01,
            gridcolor="grey",
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="orange",
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridwidth=0.01,
            gridcolor="grey",
            showline=True,
            showticklabels=True,
            tickfont=dict(
                family="Arial",
                size=12,
                color="orange",
            ),
        ),
        autosize=False,
        margin=dict(
            autoexpand=True,
            # l=100,
            # r=20,
            t=100,
        ),
    )
    st.text("")
    st.text("\n")
    return fig, plt_title
