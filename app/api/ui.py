import gradio as gr

from web.ui_lang import i18n
from app.api.backend import dialogue_synthesis_function


def build_gradio_ui() -> gr.Blocks:
    with gr.Blocks(title="FireRedTTS-2", theme=gr.themes.Default()) as page:
        # ======================== UI ========================
        title_desc = gr.Markdown(value="# {}".format(i18n("title_md_desc")))
        with gr.Row():
            lang_choice = gr.Radio(
                choices=["中文", "English"],
                value="中文",
                label="Display Language/显示语言",
                type="index",
                interactive=True,
            )
            voice_mode_choice = gr.Radio(
                choices=[i18n("voice_model_choice1"), i18n("voice_model_choice2")],
                value=i18n("voice_model_choice1"),
                label=i18n("voice_mode_label"),
                type="index",
                interactive=True,
            )
        with gr.Row():
            # ==== Speaker1 Prompt ====
            with gr.Column(scale=1):
                with gr.Group(visible=True) as spk1_prompt_group:
                    spk1_prompt_audio = gr.Audio(
                        label=i18n("spk1_prompt_audio_label"),
                        type="filepath",
                        editable=False,
                        interactive=True,
                    )
                    spk1_prompt_text = gr.Textbox(
                        label=i18n("spk1_prompt_text_label"),
                        placeholder=i18n("spk1_prompt_text_placeholder"),
                        lines=3,
                    )
            # ==== Speaker2 Prompt ====
            with gr.Column(scale=1):
                with gr.Group(visible=True) as spk2_prompt_group:
                    spk2_prompt_audio = gr.Audio(
                        label=i18n("spk2_prompt_audio_label"),
                        type="filepath",
                        editable=False,
                        interactive=True,
                    )
                    spk2_prompt_text = gr.Textbox(
                        label=i18n("spk2_prompt_text_label"),
                        placeholder=i18n("spk2_prompt_text_placeholder"),
                        lines=3,
                    )
            # ==== Text input ====
            with gr.Column(scale=2):
                dialogue_text_input = gr.Textbox(
                    label=i18n("dialogue_text_input_label"),
                    placeholder=i18n("dialogue_text_input_placeholder"),
                    lines=18,
                )
        # Generate button
        generate_btn = gr.Button(
            value=i18n("generate_btn_label"), variant="primary", size="lg"
        )
        # Long output audio
        generate_audio = gr.Audio(
            label=i18n("generated_audio_label"),
            interactive=False,
        )

        # ======================== Action ========================
        def _change_component_language(lang):
            global global_lang
            global_lang = ["zh", "en"][lang]
            return [
                gr.update(value="# {}".format(i18n("title_md_desc"))),
                gr.update(
                    choices=[i18n("voice_model_choice1"), i18n("voice_model_choice2")],
                    value=i18n("voice_model_choice1"),
                    label=i18n("voice_mode_label"),
                ),
                gr.update(label=i18n("spk1_prompt_audio_label")),
                gr.update(
                    label=i18n("spk1_prompt_text_label"),
                    placeholder=i18n("spk1_prompt_text_placeholder"),
                ),
                gr.update(label=i18n("spk2_prompt_audio_label")),
                gr.update(
                    label=i18n("spk2_prompt_text_label"),
                    placeholder=i18n("spk2_prompt_text_placeholder"),
                ),
                gr.update(
                    label=i18n("dialogue_text_input_label"),
                    placeholder=i18n("dialogue_text_input_placeholder"),
                ),
                gr.update(value=i18n("generate_btn_label")),
                gr.update(label=i18n("generated_audio_label")),
            ]

        lang_choice.change(
            fn=_change_component_language,
            inputs=[lang_choice],
            outputs=[
                title_desc,
                voice_mode_choice,
                spk1_prompt_audio,
                spk1_prompt_text,
                spk2_prompt_audio,
                spk2_prompt_text,
                dialogue_text_input,
                generate_btn,
                generate_audio,
            ],
        )

        def _change_prompt_input_visibility(voice_mode):
            enable = voice_mode == 0
            return [gr.update(visible=enable), gr.update(visible=enable)]

        voice_mode_choice.change(
            fn=_change_prompt_input_visibility,
            inputs=[voice_mode_choice],
            outputs=[spk1_prompt_group, spk2_prompt_group],
        )

        generate_btn.click(
            fn=dialogue_synthesis_function,
            inputs=[
                dialogue_text_input,
                voice_mode_choice,
                spk1_prompt_text,
                spk1_prompt_audio,
                spk2_prompt_text,
                spk2_prompt_audio,
            ],
            outputs=[generate_audio],
        )
    return page
