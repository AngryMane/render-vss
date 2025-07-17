#ifndef
#define TimeSinceDTCCleared

#include <future>

namespace TimeSinceDTCCleared {
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