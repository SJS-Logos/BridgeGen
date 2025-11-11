#pragma once
#include <memory>
#include "../IWork.h"

class WorkBridge {
public:
    explicit WorkBridge(std::unique_ptr<IWork>&& impl);
    void DoWork() const;
    ~WorkBridge();
private:
    std::unique_ptr<IWork> impl_;
};

// Proxy implementing IWork
class WorkProxy : public IWork {
public:
    explicit WorkProxy(std::unique_ptr<WorkBridge>&& bridge)
        : bridge_(std::move(bridge)) {}

    inline void DoWork() const override { bridge_->DoWork(); }

private:
    std::unique_ptr<WorkBridge> bridge_;
};

std::unique_ptr<IWork> CreateStableIWork(std::unique_ptr<IWork>&& impl);
