import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join(
        f"• {source}" for source in result["sources"]
    )

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide")

    inp = gr.Textbox(
        label="Ask a housing question"
    )

    btn = gr.Button("Ask")

    answer = gr.Textbox(
        label="Answer",
        lines=10
    )

    sources = gr.Textbox(
        label="Sources",
        lines=5
    )

    btn.click(
        handle_query,
        inputs=inp,
        outputs=[answer, sources]
    )

    inp.submit(
        handle_query,
        inputs=inp,
        outputs=[answer, sources]
    )

demo.launch()