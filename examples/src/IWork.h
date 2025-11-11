#pragma once

class IWork {
    public:
    virtual void DoWork() const = 0;
    virtual ~IWork() = default;
};
