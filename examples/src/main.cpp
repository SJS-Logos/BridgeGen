#include "generated/IWorkBridge.h"
#include "IWork.h"
#include "mywork.h"

int main()
{
   auto work = CreateIWorkBridge(CreateMyWork());
   work->DoWork();
   
}
