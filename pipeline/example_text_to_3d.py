from pipeline.kiss3d_wrapper import init_wrapper_from_config, run_text_to_3d, run_image_to_3d
import os
from pipeline.utils import logger, TMP_DIR, OUT_DIR
import time
if __name__ == "__main__":
    os.makedirs(os.path.join(OUT_DIR, 'text_to_3d'), exist_ok=True)
    os.system(f'rm -rf {TMP_DIR}/*')
    k3d_wrapper = init_wrapper_from_config('./pipeline/pipeline_config/default.yaml')

    prompts = [
    "ant animal", "crab animal",
    "bicycle", "motorcycle",
    "bird animal", "dinosaur animal",
    "car", "carriage",
    "dwarf", "minotaur",
    "gopher animal", "kangaroo animal",
    "horse animal", "horse skeleton",
    "animal", "lego animal",
    "magnolia tree", "sakura tree",
    "space marine", "ww2 soldier",
    "mermaid", "seahorse",
    "man standing", "robot standing",
    "atakebune ship", "modern yacht",
    "gothic cathedral", "hindu temple",
    "chair", "gothic throne, royal"
    ]

    for prompt in prompts:
    
        name = prompt.replace(' ', '_')
        end = time.time()
        gen_save_path, recon_mesh_path = run_text_to_3d(k3d_wrapper, prompt=prompt)
        print(f" text_to_3d time: {time.time() - end}")
        os.system(f'cp -f {gen_save_path} {OUT_DIR}/text_to_3d/{name}_3d_bundle.png')
        os.system(f'cp -f {recon_mesh_path} {OUT_DIR}/text_to_3d/{name}.glb')