import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.dates as mdates

#plt.gcf().autofmt_xdate()
#plt.tight_layout()
#plt.show()

def plot_func(cols, col, keyword, keyword_df):
    fig, ax = plt.subplots()
    sns.lineplot(ax=ax, data=keyword_df, x='month', y='roll_avg_round', palette="tab10", linewidth=2.5)
    ax.set_title(f"{keyword}", fontsize=15)
    ax.set_xlabel("Month", fontsize=10)
    ax.set_ylabel("Roll Avg Round", fontsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y' ))
    
    cols[col].pyplot(fig)
    
def plot_func_st(cols, col, keyword, keyword_df):
    chart_data = keyword_df[['month', 'roll_avg_round']]
    line_chart = st.line_chart(chart_data.set_index('month'), use_container_width=True)
    
    # Set title, xlabel, and ylabel
    st.write(f"## {keyword}")
    st.write("Month")
    st.write("Roll Avg Round")
    
    cols[col].add_container().add_widget(line_chart)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True