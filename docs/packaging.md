# Packaging the Project with Shiv

## Creating a Standalone Executable in Linux (WSL2)

If you want to generate a **self-contained executable** that does not depend on
`poetry`, you can use [`shiv`](https://shiv.readthedocs.io/en/latest/). Shiv
allows you to package your Python application into a single executable file that
can run in your Linux environment (including WSL2) without needing a virtual
environment.

### **1️⃣ Install Shiv** First, install `shiv` in your system:

```bash pip install shiv ```

### **2️⃣ Package the Project into a Single Executable** 

Run the following command in the root directory of your project:

```bash shiv -c taskcli -o taskcli . ```

- `-c taskcli`: Defines the entry point (`taskcli` in this case, which refers to
the CLI script defined in `pyproject.toml`).
- `-o taskcli`: Specifies the output file name (`taskcli`).
- `.`: Tells `shiv` to package the current directory.

### **3️⃣ Make the Executable and Move It to a Global Path**

After generating the `taskcli` executable, you need to give it execution
permissions and move it to a location accessible in your `PATH`:


```bash chmod +x taskcli mv taskcli ~/.local/bin/ ```

Alternatively, you can move it to `/usr/local/bin/` if you want it available
system-wide (requires `sudo`):

```bash sudo mv taskcli /usr/local/bin/ ```

### **4️⃣ Run the Command Without Poetry** 

Now you can execute the command directly, without needing `poetry run`:

```bash taskcli tracker ```

### **Benefits of Using Shiv** ✅ No need to activate a virtual environment.  ✅

The executable contains all necessary dependencies.  ✅ Works seamlessly inside
WSL2/Linux.  ✅ Lightweight alternative to full package distribution.

### **Additional Notes**

- The first time you run the generated `taskcli` executable, it may take a
second to initialize because `shiv` creates a temporary runtime environment.
- If you update the project, you will need to re-run the `shiv` command to
generate an updated executable.

--- This document is part of the **documentation** for this project. You can
find more details in `docs/installation.md` and `README.md`.

