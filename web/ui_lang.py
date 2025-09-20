from typing import Literal


def i18n(key):
    global global_lang
    return _i18n_key2lang_dict[key][global_lang]


# i18n
_i18n_key2lang_dict = dict(
    # Title markdown
    title_md_desc=dict(
        en="FireRedTTS-2 🔥 Dialogue Generation",
        zh="FireRedTTS-2 🔥 对话生成",
    ),
    # Voice mode radio
    voice_mode_label=dict(
        en="Voice Mode",
        zh="音色模式",
    ),
    voice_model_choice1=dict(
        en="Voice Clone",
        zh="音色克隆",
    ),
    voice_model_choice2=dict(
        en="Random Voice",
        zh="随机音色",
    ),
    # Speaker1 Prompt
    spk1_prompt_audio_label=dict(
        en="Speaker 1 Prompt Audio",
        zh="说话人 1 参考语音",
    ),
    spk1_prompt_text_label=dict(
        en="Speaker 1 Prompt Text",
        zh="说话人 1 参考文本",
    ),
    spk1_prompt_text_placeholder=dict(
        en="[S1] text of speaker 1 prompt audio.",
        zh="[S1] 说话人 1 参考文本",
    ),
    # Speaker2 Prompt
    spk2_prompt_audio_label=dict(
        en="Speaker 2 Prompt Audio",
        zh="说话人 2 参考语音",
    ),
    spk2_prompt_text_label=dict(
        en="Speaker 2 Prompt Text",
        zh="说话人 2 参考文本",
    ),
    spk2_prompt_text_placeholder=dict(
        en="[S2] text of speaker 2 prompt audio.",
        zh="[S2] 说话人 2 参考文本",
    ),
    # Dialogue input textbox
    dialogue_text_input_label=dict(
        en="Dialogue Text Input",
        zh="对话文本输入",
    ),
    dialogue_text_input_placeholder=dict(
        en="[S1]text[S2]text[S1]text...",
        zh="[S1]文本[S2]文本[S1]文本...",
    ),
    # Generate button
    generate_btn_label=dict(
        en="Generate Audio",
        zh="合成",
    ),
    # Generated audio
    generated_audio_label=dict(
        en="Generated Dialogue Audio",
        zh="合成的对话音频",
    ),
    # Warining1: invalid text for prompt
    warn_invalid_spk1_prompt_text=dict(
        en='Invalid speaker 1 prompt text, should strictly follow: "[S1]xxx"',
        zh='说话人 1 参考文本不合规，格式："[S1]xxx"',
    ),
    warn_invalid_spk2_prompt_text=dict(
        en='Invalid speaker 2 prompt text, should strictly follow: "[S2]xxx"',
        zh='说话人 2 参考文本不合规，格式："[S2]xxx"',
    ),
    # Warining2: invalid text for dialogue input
    warn_invalid_dialogue_text=dict(
        en='Invalid dialogue input text, should strictly follow: "[S1]xxx[S2]xxx..."',
        zh='对话文本输入不合规，格式："[S1]xxx[S2]xxx..."',
    ),
    # Warining3: incomplete prompt info
    warn_incomplete_prompt=dict(
        en="Please provide prompt audio and text for both speaker 1 and speaker 2",
        zh="请提供说话人 1 与说话人 2 的参考语音与参考文本",
    ),
)

global_lang: Literal["zh", "en"] = "zh"
