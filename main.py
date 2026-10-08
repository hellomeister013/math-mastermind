from hf import generate_response
import io, streamlit as st

SYSYTEM_PROMPT = """
You are a math mastermind. For every math problem:
1) Show all workings.
2) Explain each step in detail when necessary for an 8th Grader.
3) Give alternate methods to solve the problem when possible.
4) Verify the final answer and explain why it is correct.
5) If the problem is unsolvable, explain why and provide a similar solvable problem with a solution.
6) Use proper notation and markdown formatting for mathematical expressions.
"""

def math_generate(problem: str, level:str, temperature=0.1, max_tokens=1024) -> str:
    prompt = f"{SYSYTEM_PROMPT}\n\nProblem: {problem}\nLevel: {level}\n\nAnswer:"
    response = generate_response(prompt, temperature=temperature, max_tokens=max_tokens)
    return response

def export_txt(history):
    txt = "\n\n".join([f"Problem: {item['problem']}\nLevel: {item['level']}\nAnswer:\n{item['answer']}" for item in history])
    return io.BytesIO(txt.encode('utf-8'))

def setup_ui():
    st.set_page_config(page_title="Math Problem Solver", page_icon=":abacus:", layout="wide")
    st.title("Math Problem Solver")
    st.write("Enter a math problem and select the difficulty level to get a detailed solution.")

    with st.expander("Example"):
        st.markdown(
            '- Algebra: "Solve 2x² - 4x + 2 = 0"\n'
            '- Geometry: "Find the area of a circle with radius 5"\n'
            '- Calculus: "Find the derivative of x² + 3x + 2"'
        )

    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", 0)

    c1, c2 = st.columns([1,2])
    if c1.button("Clear History"):
        st.session_state.history = []
        st.session_state.k = 0

    if c2.button("Export History"):
        c2.download_button(
            label="Download History as TXT",
            data=export_txt(st.session_state.history),
            file_name="math_history.txt",
            mime="text/plain"
        )

    with st.form("

    