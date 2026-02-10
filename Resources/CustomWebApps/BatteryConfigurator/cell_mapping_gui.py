import tkinter as tk
from tkinter import messagebox

class CellMappingGUI:
    def __init__(self, root):
        self.root = root
        # Allow grid expansion
        for i in range(10):
            self.root.columnconfigure(i, weight=1)

        for i in range(6):
            self.root.rowconfigure(i, weight=1)

        self.root.title("Battery Cell Mapper → Modelica")

        # ================= INPUTS =================
        labels = ["Ns", "Np", "Rows", "Columns"]
        self.entries = []

        for i, text in enumerate(labels):
            tk.Label(root, text=text).grid(row=0, column=2*i, padx=4)
            e = tk.Entry(root, width=5)
            e.grid(row=0, column=2*i+1)
            self.entries.append(e)

        tk.Button(root, text="Create Grid", command=self.create_grid)\
            .grid(row=0, column=8, padx=10)

        tk.Label(root, text="Parallel Group (p)").grid(row=1, column=0)
        self.p_entry = tk.Entry(root, width=5)
        self.p_entry.grid(row=1, column=1)
        self.p_entry.insert(0, "1")

        # ================= SCROLLABLE GRID =================
        self.canvas = tk.Canvas(root, height=350)
        self.canvas.grid(row=2, column=0, columnspan=9, sticky="nsew")

        self.v_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.grid(row=2, column=9, sticky="ns")

        self.h_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=3, column=0, columnspan=9, sticky="ew")

        self.canvas.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )

        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # ================= OUTPUT WITH SCROLL =================
        output_frame = tk.Frame(root)
        output_frame.grid(row=4, column=0, columnspan=9, sticky="nsew", pady=10)

        self.out_scroll = tk.Scrollbar(output_frame)
        self.out_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.output = tk.Text(
            output_frame,
            height=8,
            width=80,
            yscrollcommand=self.out_scroll.set
        )
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.out_scroll.config(command=self.output.yview)

        # ================= INTERNAL STATE =================
        self.mapping = {}
        self.series_counter = 1

    # ================= CREATE GRID =================
    def create_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        try:
            self.ns = int(self.entries[0].get())
            self.np = int(self.entries[1].get())
            self.rows = int(self.entries[2].get())
            self.cols = int(self.entries[3].get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid integers")
            return

        self.mapping.clear()
        self.series_counter = 1
        self.output.delete("1.0", tk.END)

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.grid_frame,
                    text="+",
                    width=6,
                    height=2,
                    bg="lightgray",
                    command=lambda r=r, c=c: self.assign_cell(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)

    # ================= ASSIGN CELL =================
    def assign_cell(self, row, col):
        btn = self.grid_frame.grid_slaves(row=row, column=col)[0]

        try:
            p = int(self.p_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Parallel group must be integer")
            return

        if (row, col) not in self.mapping:
            if self.series_counter > self.ns * self.np:
                messagebox.showinfo("Info", "All electrical cells assigned")
                return

            self.mapping[(row, col)] = {
                "s": self.series_counter,
                "p": p,
                "x": row + 1,   # rows → x
                "y": col + 1    # columns → y
            }

            btn.config(text=str(self.series_counter), bg="red", fg="white")
            self.series_counter += 1
        else:
            self.mapping[(row, col)]["p"] = p
            btn.config(bg="orange")

        self.update_modelica()

    # ================= MODELICA OUTPUT =================
    def update_modelica(self):
        data = sorted(self.mapping.values(), key=lambda d: d["s"])

        rows = []
        for d in data:
            rows.append(f"{d['s']},{d['p']},{d['x']},{d['y']}")

        modelica_array = "[" + ";".join(rows) + "]"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, modelica_array)


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    CellMappingGUI(root)
    root.mainloop()