#pragma once
#include <memory>
#include "../IWork.h"

namespace detail {

// Hidden bridge (not part of public ABI)
class IWorkBridge {
public:
    explicit IWorkBridge(std::unique_ptr<IWork>&& impl)
        : impl_(std::move(impl)) {}

    void DoWork() const { impl_->DoWork(); }

private:
    std::unique_ptr<IWork> impl_;
};

} // namespace detail

// Proxy implementing IWork
class IWorkProxy : public IWork {
public:
    explicit IWorkProxy(std::unique_ptr<detail::IWorkBridge>&& bridge)
        : bridge_(std::move(bridge)) {}

    inline void DoWork() const override { bridge_->DoWork(); }

private:
    std::unique_ptr<detail::IWorkBridge> bridge_;
};

// Inline factory (header-only)
inline std::unique_ptr<IWork> CreateStableIWork(std::unique_ptr<IWork>&& impl) {
    auto bridge = std::make_unique<detail::IWorkBridge>(std::move(impl));
    return std::make_unique<IWorkProxy>(std::move(bridge));
}
