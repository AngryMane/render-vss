#ifndef
#define LongTermO2Trim1

#include <future>

namespace LongTermO2Trim1 {
  class Sensor {
     get();
    std::future<bool> set( value);
    int subscribe();
    void unsubscribe(int subscribe_token);
    int try_lock();
    int unlock(int lock_token);
  }
}

#endif 