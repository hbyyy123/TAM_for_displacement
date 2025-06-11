<!-- ![](./assets/track-anything-logo.jpg) -->

<div align=center>
<img src="./assets/track-anything-logo.jpg"/>
</div>
<br/>
<div align=center>
<a src="https://img.shields.io/badge/%F0%9F%93%96-Arxiv_2304.11968-red.svg?style=flat-square" href="https://arxiv.org/abs/2304.11968">
<img src="https://img.shields.io/badge/%F0%9F%93%96-Arxiv_2304.11968-red.svg?style=flat-square">
</a>
<a src="https://img.shields.io/badge/%F0%9F%A4%97-Open_in_Spaces-informational.svg?style=flat-square" href="https://huggingface.co/spaces/VIPLab/Track-Anything?duplicate=true">
<img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging_Face_Space-informational.svg?style=flat-square">
</a>
<a src="https://img.shields.io/badge/%F0%9F%97%BA-Tutorials in Steps-2bb7b3.svg?style=flat-square" href="./doc/tutorials.md">
<img src="https://img.shields.io/badge/%F0%9F%97%BA-Tutorials in Steps-2bb7b3.svg?style=flat-square">

</a>
<a src="https://img.shields.io/badge/%F0%9F%9A%80-SUSTech_VIP_Lab-ed6c00.svg?style=flat-square" href="https://zhengfenglab.com/">
<img src="https://img.shields.io/badge/%F0%9F%9A%80-SUSTech_VIP_Lab-ed6c00.svg?style=flat-square">
</a>
</div>
> ⚠️ This README has been modified to reflect project-specific adjustments for displacement tracking.

> It includes updated environment requirements (Python 3.10) and custom checkpoints setup instructions.

***Track-Anything*** is a flexible and interactive tool for video object tracking and segmentation. It is developed upon [Segment Anything](https://github.com/facebookresearch/segment-anything), can specify anything to track and segment via user clicks only. During tracking, users can flexibly change the objects they wanna track or correct the region of interest if there are any ambiguities. These characteristics enable ***Track-Anything*** to be suitable for: 
- Video object tracking and segmentation with shot changes. 
- Visualized development and data annotation for video object tracking and segmentation.
- Object-centric downstream video tasks, such as video inpainting and editing. 

<div align=center>
<img src="./assets/avengers.gif" width="81%"/>
</div>

<!-- ![avengers]() -->

## :rocket: Updates

- 2023/05/02: We uploaded tutorials in steps :world_map:. Check [HERE](./doc/tutorials.md) for more details.

- 2023/04/29: We improved inpainting by decoupling GPU memory usage and video length. Now Track-Anything can inpaint videos with any length! :smiley_cat: Check [HERE](https://github.com/gaomingqi/Track-Anything/issues/4#issuecomment-1528198165) for our GPU memory requirements. 

- 2023/04/25: We are delighted to introduce [Caption-Anything](https://github.com/ttengwang/Caption-Anything) :writing_hand:, an inventive project from our lab that combines the capabilities of Segment Anything, Visual Captioning, and ChatGPT. 

- 2023/04/20: We deployed [DEMO](https://huggingface.co/spaces/VIPLab/Track-Anything?duplicate=true) on Hugging Face :hugs:!

- 2023/04/14: We made Track-Anything public!

## :world_map: Video Tutorials ([Track-Anything Tutorials in Steps](./doc/tutorials.md))

https://user-images.githubusercontent.com/30309970/234902447-a4c59718-fcfe-443a-bd18-2f3f775cfc13.mp4

---

### :joystick: Example - Multiple Object Tracking and Segmentation (with [XMem](https://github.com/hkchengrex/XMem))

https://user-images.githubusercontent.com/39208339/233035206-0a151004-6461-4deb-b782-d1dbfe691493.mp4

---

### :joystick: Example - Video Object Tracking and Segmentation with Shot Changes (with [XMem](https://github.com/hkchengrex/XMem))

https://user-images.githubusercontent.com/30309970/232848349-f5e29e71-2ea4-4529-ac9a-94b9ca1e7055.mp4

---

### :joystick: Example - Video Inpainting (with [E2FGVI](https://github.com/MCG-NKU/E2FGVI))

https://user-images.githubusercontent.com/28050374/232959816-07f2826f-d267-4dda-8ae5-a5132173b8f4.mp4
---

## 🔧 Environment Update (TAM version)

This repository has been adapted for our displacement-tracking project and now uses:

- ✅ **Python 3.10**
- ✅ Updated `requirements.txt` with minimal, clean dependencies
- ✅ **cuda version--12.4**

To recreate the environment:

```bash
conda create -n tam python=3.10 -y
conda activate tam
pip install -r requirements.txt
```
## :computer: Get Started
#### Linux & Windows
```shell
# Clone the repository:
git clone https://github.com/gaomingqi/Track-Anything.git
cd Track-Anything

# Install dependencies: 
pip install -r requirements.txt

# Run the Track-Anything gradio demo.
python app.py --device cuda:0
# python app.py --device cuda:0 --sam_model_type vit_b # for lower memory usage
```
## :file_folder: Checkpoints Requirement

Before running the tracking or inpainting modules, please manually create a folder named `checkpoints` in the project root and place the following pre-trained model files inside:

- `sam_vit_h_4b8939.pth` – Segment Anything Model (SAM)  
- `XMem-s012.pth` – XMem memory network for long-term tracking  
- `E2FGVI-CVPR22.pth` – Inpainting model

```bash
mkdir checkpoints
# Place all .pth files inside this folder
```
## :wrench: Custom Scripts for Displacement Tracking

The following Python scripts were added to this repository to support displacement tracking analysis:

- `disp_output_point.py`  
  → Extracts displacement directly from masked video frames by detecting mask colors.  
  ✅ Suitable for cases where masks are clearly visible and uniformly colored.

- `calc_centroid_disp.py`  
  → Computes displacement by calculating the centroid from per-frame `.npy` mask files.

- `show_npy.py`  
  → Visualizes `.npy` mask files frame-by-frame for inspection and verification.

> These scripts were developed specifically for the displacement-tracking extension of the Track-Anything project.


## :book: Citation
If you find this work useful for your research or applications, please cite using this BibTeX:
```bibtex
@misc{yang2023track,
      title={Track Anything: Segment Anything Meets Videos}, 
      author={Jinyu Yang and Mingqi Gao and Zhe Li and Shang Gao and Fangjing Wang and Feng Zheng},
      year={2023},
      eprint={2304.11968},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## :clap: Acknowledgements

The project is based on [Segment Anything](https://github.com/facebookresearch/segment-anything), [XMem](https://github.com/hkchengrex/XMem), and [E2FGVI](https://github.com/MCG-NKU/E2FGVI). Thanks for the authors for their efforts.
