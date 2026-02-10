# Battery Cell Mapper → Modelica

A lightweight, browser-based utility designed to bridge the gap between physical battery pack layouts and **Modelica** electrical simulations. This tool allows users to visually map the physical location ($x, y$ coordinates) of battery cells to their specific electrical series and parallel positions.



##  Live Demo
https://abhilashknair.github.io/battery-configurator/

##  Overview
When simulating large battery packs in Modelica, a common requirement is an array that defines the relationship between a cell's electrical index and its physical position (often for thermal coupling). This tool provides a GUI to generate that array without manual data entry.

### Features
* **Dynamic Grid Generation**: Define custom rows and columns to match your physical module layout.
* **Sequential Mapping**: Automatically increments series indices ($s$) as you click each cell.
* **Parallel Grouping**: Assign cells to specific parallel groups ($p$) on the fly.
* **Real-time Modelica Output**: Generates a formatted array string: `[s, p, x, y; ...]`.
* **Excel Export**: Download your configuration as an `.xlsx` file for documentation or automated post-processing.

---

##  How to Use

1. **Initialize the Pack**: 
   * Enter the total number of series cells (**Ns**) and parallel cells (**Np**).
   * Define the physical **Rows** and **Columns** of your module.
   * Click **Create Grid**.

2. **Map the Cells**:
   * Set the **Current Parallel Group (p)** value.
   * Click the buttons in the grid in the order they are electrically connected.
   * The button will turn **Red** and display the series index ($s$).

3. **Adjusting Data**:
   * If you need to update the parallel group for an assigned cell, change the $p$ value in the input field and click the cell again. It will turn **Orange** to indicate the update.

4. **Export**:
   * **Copy Text**: Copies the Modelica-ready string to your clipboard.
   * **Export to Excel**: Downloads an `.xlsx` file containing the mapping table.

---

##  Data Format
The output follows the standard Modelica matrix format for battery management and thermal libraries:

$$[s, p, x, y]$$

| Variable | Description |
| :--- | :--- |
| **s** | **Series Index**: The electrical sequence number of the cell. |
| **p** | **Parallel Group**: The index of the parallel string the cell belongs to. |
| **x** | **Row Coordinate**: Physical row position (starting at 1). |
| **y** | **Column Coordinate**: Physical column position (starting at 1). |

---

##  Technical Stack
* **Frontend**: HTML5, JavaScript (ES6+).
* **Styling**: [Tailwind CSS](https://tailwindcss.com/) (Utility-first CSS framework).
* **Excel Logic**: [SheetJS (xlsx)](https://sheetjs.com/) for client-side file generation.
* **Hosting**: [GitHub Pages](https://pages.github.com/) (Static site hosting).

##  License
This project is open-source and available under the [MIT License](LICENSE).
