#
# Copyright (c) 2021-2024, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
#

import os
import sys
from pathlib import Path

import numpy as np
import tensorrt as trt

sys.path.append("/trtcookbook/include")
from utils import TRTWrapperV1, case_mark

trt_file = Path("model.trt")
data = {"inputT0": np.arange(3 * 4 * 5, dtype=np.float32).reshape(3, 4, 5)}

@case_mark  # This wrapper does nothing but printing case information in stdout.
def case_build_and_run():
    tw = TRTWrapperV1()  # We use TRTWrapper to simplify API calls.

    input_tensor = tw.network.add_input("inputT0", trt.float32, [-1, -1, -1])
    tw.profile.set_shape(input_tensor.name, [1, 1, 1], [3, 4, 5], [6, 8, 10])
    tw.config.add_optimization_profile(tw.profile)

    identity_layer = tw.network.add_identity(input_tensor)

    tw.build([identity_layer.get_output(0)])
    tw.serialize_engine(trt_file)

    tw.setup(data)
    tw.infer()

@case_mark
def case_load_and_run():
    tw = TRTWrapperV1(trt_file=trt_file)

    tw.setup(data)
    tw.infer()

if __name__ == "__main__":
    os.system("rm -rf *.trt")

    case_build_and_run()
    case_load_and_run()

    print("Finish")
