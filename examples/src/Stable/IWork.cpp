#include <memory>
#include "IWork.h"

WorkBridge::WorkBridge(std::unique_ptr<IWork>&& impl) : impl_(std::move(impl)) {}
void WorkBridge::DoWork() const { impl_->DoWork(); }
WorkBridge::~WorkBridge() {}

std::unique_ptr<IWork> CreateStableIWork(std::unique_ptr<IWork>&& impl)
{
    auto bridge = std::make_unique<WorkBridge>(std::move(impl));
    return std::make_unique<IWorkProxy>(std::move(bridge));
}
