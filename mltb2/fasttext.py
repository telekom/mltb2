# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""fastText specific functionality.

This module is based on `fastText <https://fasttext.cc/docs/en/support.html>`_.
Use pip to install the necessary dependencies for this module:
``pip install mltb2[fasttext]``
"""

import os
from dataclasses import dataclass, field

import fasttext
from fasttext.FastText import _FastText

from mltb2.files import fetch_remote_file, get_and_create_mltb2_data_dir


@dataclass
class FastTextLanguageIdentification:
    """Identify languages of a text."""

    model: _FastText = field(init=False, repr=False)

    def __post_init__(self):
        """Do post init."""
        self.model = fasttext.load_model(self.get_model_path_and_download())

    @staticmethod
    def get_model_path_and_download() -> str:
        """Get the model path and download it if needed."""
        model_filename = "lid.176.bin"
        mltb2_data_home = get_and_create_mltb2_data_dir()
        model_full_path = os.path.join(mltb2_data_home, model_filename)
        if not os.path.exists(model_full_path):
            model_url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
            sha256_checksum = "7e69ec5451bc261cc7844e49e4792a85d7f09c06789ec800fc4a44aec362764e"
            fetch_remote_file_path = fetch_remote_file(
                dirname=mltb2_data_home,
                filename=model_filename,
                url=model_url,
                sha256_checksum=sha256_checksum,
            )
            assert fetch_remote_file_path == model_full_path  # noqa: S101

        return model_full_path

    def __call__(self, text, num_lang: int = 10):
        """Identify languages of a given text.

        Args:
            text: the text for which the language is to be recognized
            num_lang: number of returned languages
        Returns:
            A dict from language to probability.
            This dict contains no more than ``num_lang`` elements.
            So it is not guaranteed that the language you want to recognize is
            included in the dict. This is the case when the probability is very low.
            Possible languages are: ``af als am an ar arz as ast av az azb ba bar
            bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co cs cv cy da de
            diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom
            gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk
            km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min
            mk ml mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or
            os pa pam pfl pl pms pnb ps pt qu rm ro ru rue sa sah sc scn sco sd sh
            si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec
            vep vi vls vo wa war wuu xal xmf yi yo yue zh``
        """
        predictions = self.model.predict(text, k=num_lang)
        languages = predictions[0]
        probabilities = predictions[1]
        lang_to_prob = {lang[9:]: prob for lang, prob in zip(languages, probabilities)}
        return lang_to_prob
