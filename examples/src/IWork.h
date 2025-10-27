#pragma once

// Public stable interface 
class IWork {
    public:
    virtual void DoWork() const = 0;
    virtual ~IWork() = default;
};
