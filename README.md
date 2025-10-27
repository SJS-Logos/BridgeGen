# BridgeGen — Generate ABI-Stable Bridge Classes for C++

**BridgeGen** is a single-file Python utility that generates *non-virtual bridge classes*
wrapping C++ abstract interfaces.  

The generated bridge separates the *stable* interface used by clients
from the *abstract* interface implemented in back-end modules.

This tool implements what we call the **Stable Interface Bridge** —
a practical combination of:
- the **Bridge** pattern (GoF),
- the **Pimpl** (compilation-firewall idiom), and
- an **Abstract Factory** for instance creation.

---

## ✨ Example

Input file `IWork.h`:

```cpp
class IWork {
public:
    virtual void DoWork() = 0;
    virtual ~IWork() = default;
};
```

Run BridgeGen:

```bash
python bridgegen.py IWork.h
```

Output files:

- `IWorkBridge.h`
- `IWorkBridge.cpp`

Generated header (excerpt):

```cpp
#pragma once
#include <memory>

class IWork;

class IWorkBridge {
public:
    explicit IWorkBridge(std::unique_ptr<IWork>&& impl);
    ~IWorkBridge();

    void DoWork();

private:
    std::unique_ptr<IWork> impl_;
};

// Factory constructor
std::unique_ptr<IWorkBridge> CreateIWorkBridge(std::unique_ptr<IWork>&& impl);
```

---

## 🚀 Installation

BridgeGen is **a single Python file** — no templates or extra data files.

### Requirements
- Python 3.7 or newer  
- Standard library only (no third-party packages)

### Clone and run

```bash
git clone https://github.com/SJS-Logos/BridgeGen.git
cd BridgeGen
python bridgegen.py path/to/YourInterface.h
```

---

## 🧩 How it works

BridgeGen:
1. Parses your header to find the first **abstract class**
   (a `class` containing at least one `virtual … = 0;`).
2. Extracts all pure-virtual methods.
3. Emits a *Bridge* pair of files:
   - a `.h` containing only a forward declaration of the interface;
   - a `.cpp` that includes both the bridge and interface headers.

This isolates your ABI from implementation changes and avoids recompilation cascades.

---

## 🧱 Pattern Summary

The **Stable Interface Bridge** pattern combines:
| Idiom | Purpose |
|-------|----------|
| **Abstract Interface** | Defines the contract between client and module |
| **Pimpl / Opaque Pointer** | Hides concrete implementation types |
| **Bridge** | Decouples stable façade from polymorphic backend |
| **Factory Function** | Simplifies construction and lifetime management |

Advantages:
- ABI-safe: no vtable exposure in client headers  
- Cleaner module boundaries  
- Explicit ownership (`std::unique_ptr`)  
- Automatically generated boilerplate  

---

## ⚖️ License

MIT License — free to use, modify, and redistribute.

---

## 📚 References

- *The Pimpl Pattern — What You Should Know* by Bartek Filipek (cppstories.com)  
- *Herb Sutter: Compilation Firewalls*  
- *Design Patterns* — Gamma et al. (Bridge pattern)  
- *C++ Core Guidelines*: “Pimpl and ABI stability”  

---

## 🧠 Maintainers

Created by **Steen Sannung**.  
Contributions and pull requests welcome!
