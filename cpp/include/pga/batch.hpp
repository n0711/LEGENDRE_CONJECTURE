#pragma once
#include "interval.hpp"
#include <atomic>
#include <future>

namespace pga::library {
// ESTABLISHED: each input interval is independent; output order matches input.
inline std::vector<Result> count_batch(const std::vector<u64>& inputs,
                                       std::size_t workers,
                                       std::size_t block=65536) {
    if (!workers || !block) throw std::invalid_argument("positive workers and block required");
    for (auto n:inputs) validate(n,block);
    std::vector<Result> results(inputs.size());
    std::atomic<std::size_t> next{0};
    std::vector<std::future<void>> tasks;
    const auto active=std::min(workers,inputs.size());
    tasks.reserve(active);
    for (std::size_t w=0;w<active;++w) {
        tasks.push_back(std::async(std::launch::async,[&] {
            for (;;) {
                const auto i=next.fetch_add(1,std::memory_order_relaxed);
                if (i>=inputs.size()) return;
                results[i]=count(inputs[i],block);
            }
        }));
    }
    for (auto& task:tasks) task.get();
    return results;
}
} // namespace pga::library
