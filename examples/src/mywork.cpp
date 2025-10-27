#include <iostream>
#include <memory>
#include "IWork.h"

class MyWork : public IWork {
public:
    void DoWork() const override { 
      std::cout << "Do something" << std::endl;
    }
};

std::unique_ptr<IWork> CreateMyWork()
{
   return std::make_unique<MyWork>();
}
