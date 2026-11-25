
# Tract Shape Analysis (tcks2tractmeasures)

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Computes tract shape measures (length, span, area, volume, elongation, curvature, torsion and more) for each tract in a tcks folder with DSI Studio and DIPY and merges them into one tractmeasures CSV.**

Converts each .tck to .trk using a reference image, computes geometric shape statistics with DSI Studio and curvature/torsion with DIPY, and stacks and merges them into stat/tractmeasures.csv. Only one reference image is needed: the first available of T1w, T2w, parcellation or mask is used. Use it to characterise tract morphology for group analyses.

| | |
|---|---|
| 📥 **Inputs** | `neuro/tcks` · `neuro/anat/t1w` (optional) · `neuro/anat/t2w` (optional) · `neuro/mask` (optional) · `neuro/parcellation/volume` (optional) |
| 📤 **Outputs** | `neuro/tractmeasures` |
| 🐳 **Container** | `brainlife/dipy:1.4.1` |
| ⚙️ **Resources** | 1 CPUs · 0.92 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.844](https://doi.org/10.25663/brainlife.app.844) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `tcks` | `neuro/tcks` | yes | Directory of per-tract .tck files. Must contain at least one .tck file. |
| `t1` | `neuro/anat/t1w` | no | T1-weighted reference image (used first if present). |
| `t2` | `neuro/anat/t2w` | no | T2-weighted reference image (used if no T1w is given). |
| `mask` | `neuro/mask` | no | Mask used as reference image if no anatomical image is given. |
| `parc` | `neuro/parcellation/volume` | no | Parcellation used as reference image if no anatomical image is given. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `stat` | `neuro/tractmeasures` | Tract measures table (tractmeasures.csv) with one row per tract and DSI Studio and DIPY shape metrics. |

<!-- brainlife-app:end -->

`tcks2tractmeasures` is a pipeline for processing and analyzing tractography data. It computes a range of tract-specific metrics using **DSI Studio** (for geometric measures like length, area, and elongation) and **DIPY** (for advanced measures like curvature and torsion). Results are exported as structured statistics for further analysis.

---

## Author

**Gabriele Amorosino**  
*Email*: gabriele.amorosino@utexas.edu  

---

## Usage

### Running on Brainlife.io

You can run the `tcks2tractmeasures` app on the [Brainlife.io platform](https://brainlife.io) via the web user interface (UI) or using the Brainlife CLI. This platform manages inputs and outputs and executes computations on its cloud resources.

#### On Brainlife.io via UI

1. Navigate to the Brainlife.io platform and locate the `app-tcks2tractmeasures` app.
2. Click the **Execute** tab.
3. Upload the required input files:
   - A folder containing _.tck_ files, encoded in BrainLife as `tcks` datatype.
   - A reference image such as t1w, t2w, mask or parcellation.
4. Submit the job and eventually download or visualize the results after computation completes.

#### On Brainlife.io using CLI

1. Install the Brainlife CLI by following the instructions [here](https://brainlife.io/docs/cli/install/).
2. Log in to the Brainlife CLI:
   ```bash
   bl login
   ```
3. Execute the app with the following command:
   ```bash
   bl app run --id 67858b5e81d348aa56483324 --project <project_id> --input tcks:<tcks_id> --input reference:<reference_id>
   ```
   Replace `<project_id>`, and input IDs with the appropriate values. The output will be saved in the specified project.

---

### Running Locally

You can run the pipeline locally either by using a configuration file or by directly passing the input paths.

#### **Option 1: Using a Configuration File**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gamorosino/app-tcks2tractmeasures.git
   cd app-tcks2tractmeasures
   ```

2. **Prepare a `config.json` file** to specify input paths and output options. Example:
   ```json
   {
       "tcks": "/path/to/tcks",
       "t1": "/path/to/t1.nii"
   }
   ```

3. **Execute the script:**
   ```bash
   ./main
   ```

The results will be saved in the `./stat/tractmeasures.csv` relative to the directory where the script is executed.

#### **Option 2: Using `main.sh` Script**

Alternatively, you can use the `main.sh` script, which avoids the use of a `config.json` file by directly taking the full paths of the input files as arguments:

   ```bash
   ./main.sh <tractogram.tck> <anatomy_image.nii> [outputdir]
   ```

- `<tractogram.tck>`: Path to the TCK file(s) folder.
- `<anatomy_image.nii>`: Path to the anatomical file (NIfTI format).
- `[outputdir]` (optional): Path to the output directory where the results will be stored. If not provided, the results are saved in the same directory where the script is executed. 
If the `outputdir` is not specified, the results will be saved in the `./stat/tractmeasures.csv` relative to the directory where the script is executed.

---

## Outputs

The results are saved in the `stat/tractmeasures.csv` file, which includes:
  - **Geometric Measures**: Metrics such as length, span, volume, diameter, surface area, curl, elongation, and irregularity, calculated using DSI Studio.
  - **Streamline Properties**: Average curvature and torsion values, computed using DIPY.

---

## Requirements

- Singularity

---

## Citation

If you use this repository in your research, please cite the following:

- **DSI Studio**:  
  Yeh, F.-C. (2020). Shape analysis of the human association pathways.  
  *Neuroimage, 223*, 117329.  
  [DOI: 10.1016/j.neuroimage.2020.117329](https://doi.org/10.1016/j.neuroimage.2020.117329)

- **DIPY**:  
  Garyfallidis, E., et al. (2014). DIPY, a library for the analysis of diffusion MRI data.  
  *Frontiers in Neuroinformatics, 8*, 8.  
  [DOI: 10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008)

- **Brainlife.io**:  
  Hayashi, S., et al. (2024). brainlife.io: a decentralized and open-source cloud platform to support neuroscience research.  
  *Nature Methods, 21*(5), 809-813.  
  [DOI: 10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)

---

## Acknowledgments
The script for converting tck files to trk (tck2trk.py) is based on the work of Marc-Alexandre Côté (https://gist.github.com/MarcCote/ea6842cc4c3950f7596fc3c8a0be0154).
