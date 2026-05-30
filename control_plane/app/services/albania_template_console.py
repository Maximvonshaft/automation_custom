from __future__ import annotations

from pathlib import Path
from tkinter import BooleanVar, StringVar, Tk, filedialog, messagebox, ttk

from control_plane.app.services.albania_batch_compiler import (
    BatchCompileOptions,
    compile_broker_excel_batch,
)
from control_plane.app.services.albania_excel_template_parser import TemplateDefaults


class AlbaniaTemplateConsole:
    def __init__(self, root: Tk) -> None:
        self.root = root
        root.title("CustomsOps Albania Template Pilot Console")
        root.geometry("820x520")

        self.excel_path = StringVar()
        self.output_dir = StringVar(value=str(Path.cwd() / "outputs" / "albania_template_pilot"))
        self.tenant_id = StringVar(value="tenant_demo")
        self.machine_id = StringVar(value="machine_demo")
        self.customs_office = StringVar(value="AL111000")
        self.authorization_reference = StringVar()
        self.truck_registration_plate_number = StringVar()
        self.include_store_safebrake = BooleanVar(value=True)
        self.status = StringVar(value="Select broker Excel template and compile plans.")

        self._build_layout()

    def _build_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Broker Excel template").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.excel_path, width=82).grid(row=0, column=1, sticky="we")
        ttk.Button(frame, text="Browse", command=self._browse_excel).grid(row=0, column=2, padx=6)

        ttk.Label(frame, text="Output directory").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(frame, textvariable=self.output_dir, width=82).grid(
            row=1,
            column=1,
            sticky="we",
            pady=(8, 0),
        )
        ttk.Button(frame, text="Browse", command=self._browse_output_dir).grid(
            row=1,
            column=2,
            padx=6,
            pady=(8, 0),
        )

        ttk.Separator(frame).grid(row=2, column=0, columnspan=3, sticky="we", pady=14)

        fields = [
            ("Tenant ID", self.tenant_id),
            ("Machine ID", self.machine_id),
            ("Customs Office", self.customs_office),
            ("Authorization Reference", self.authorization_reference),
            ("Truck Registration Plate", self.truck_registration_plate_number),
        ]
        for index, (label, variable) in enumerate(fields, start=3):
            ttk.Label(frame, text=label).grid(row=index, column=0, sticky="w", pady=4)
            ttk.Entry(frame, textvariable=variable, width=45).grid(
                row=index,
                column=1,
                sticky="w",
                pady=4,
            )

        ttk.Checkbutton(
            frame,
            text="Include SafeBrake Store action (currency intentionally blank)",
            variable=self.include_store_safebrake,
        ).grid(row=8, column=1, sticky="w", pady=(8, 0))

        ttk.Button(frame, text="Compile Batch Plans", command=self._compile).grid(
            row=9, column=1, sticky="w", pady=18
        )

        ttk.Label(frame, textvariable=self.status, wraplength=760).grid(
            row=10, column=0, columnspan=3, sticky="we", pady=(8, 0)
        )

        note = (
            "Boundary: this console compiles server-side pilot job plans only. "
            "It does not submit, register, pay, or run ASYCUDA. "
            "Currency / Monedha remains intentionally blank for SafeBrake."
        )
        ttk.Label(frame, text=note, wraplength=760).grid(
            row=11,
            column=0,
            columnspan=3,
            sticky="we",
        )

        frame.columnconfigure(1, weight=1)

    def _browse_excel(self) -> None:
        path = filedialog.askopenfilename(
            title="Select broker Excel template",
            filetypes=[("Excel files", "*.xlsx *.xlsm"), ("All files", "*.*")],
        )
        if path:
            self.excel_path.set(path)

    def _browse_output_dir(self) -> None:
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.output_dir.set(path)

    def _compile(self) -> None:
        try:
            if not self.excel_path.get().strip():
                raise ValueError("Excel template path is required.")
            if not self.authorization_reference.get().strip():
                raise ValueError("Authorization Reference is required.")
            if not self.truck_registration_plate_number.get().strip():
                raise ValueError("Truck Registration Plate is required.")

            defaults = TemplateDefaults(
                customs_office=self.customs_office.get().strip() or "AL111000",
                authorization_reference=self.authorization_reference.get().strip(),
                truck_registration_plate_number=self.truck_registration_plate_number.get().strip(),
            )
            compiled = compile_broker_excel_batch(
                Path(self.excel_path.get()),
                Path(self.output_dir.get()),
                options=BatchCompileOptions(
                    tenant_id=self.tenant_id.get().strip() or "tenant_demo",
                    machine_id=self.machine_id.get().strip() or "machine_demo",
                    include_store_safebrake=self.include_store_safebrake.get(),
                    defaults=defaults,
                ),
            )
            self.status.set(
                f"Compiled {compiled.group_count} group(s). Manifest: {compiled.manifest_path}"
            )
            messagebox.showinfo("Compilation complete", self.status.get())
        except Exception as exc:
            self.status.set(f"Compilation failed: {type(exc).__name__}: {exc}")
            messagebox.showerror("Compilation failed", self.status.get())


def main() -> int:
    root = Tk()
    AlbaniaTemplateConsole(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
