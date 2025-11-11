#include "Stable/IWork.h"
#include "IWork.h"
#include "mywork.h"

int main()
{
   auto work = CreateStableIWork(CreateMyWork());
   work->DoWork();
   
}
