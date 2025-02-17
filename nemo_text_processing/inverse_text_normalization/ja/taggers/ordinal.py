# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pynini
from pynini.lib import pynutil

from nemo_text_processing.inverse_text_normalization.ja.graph_utils import GraphFst


class OrdinalFst(GraphFst):
    """
    Finite state transducer for classifying cardinals
        e.g. 第二十三 -> cardinal { morphsyntactic_feature: "第" integer: "23" }
        e.g. 百番目 -> cardinal { integer: "100" morphsyntactic_feature:"番目" }
    """

    def __init__(self, cardinal: GraphFst):
        super().__init__(name="ordinal", kind="classify")

        cardinals = cardinal.just_cardinals
        ordinals = pynini.accep("第") | pynini.accep("番目")

        integer_component = (
            pynutil.insert("integer: \"") + ((cardinals + ordinals) | (ordinals + cardinals)) + pynutil.insert("\"")
        )

        final_graph = self.add_tokens(integer_component)
        self.fst = final_graph.optimize()
