#include "frame_id_tracker.h"

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <map>
#include <mutex>
#include <sstream>
#include <vector>

namespace gr {
namespace lora_sdr_fmcw_0 {
namespace frame_id_tracker {
namespace {

bool parse_frame_id(const std::string& message, int* frame_id)
{
    if (frame_id == nullptr)
        return false;

    const std::size_t colon_pos = message.find_last_of(':');
    std::size_t start = (colon_pos == std::string::npos) ? 0 : (colon_pos + 1);
    while (start < message.size() && std::isspace(static_cast<unsigned char>(message[start])))
        ++start;

    if (start >= message.size())
        return false;

    char* end_ptr = nullptr;
    const long parsed = std::strtol(message.c_str() + start, &end_ptr, 10);
    if (end_ptr == message.c_str() + start)
        return false;

    while (end_ptr != nullptr && *end_ptr != '\0' && std::isspace(static_cast<unsigned char>(*end_ptr)))
        ++end_ptr;
    if (end_ptr != nullptr && *end_ptr != '\0')
        return false;

    *frame_id = int(parsed);
    return true;
}

std::string summarize_ids(const std::vector<int>& ids)
{
    if (ids.empty())
        return "-";

    std::ostringstream oss;
    const std::size_t limit = std::min<std::size_t>(ids.size(), 6);
    for (std::size_t i = 0; i < limit; ++i)
    {
        if (i != 0)
            oss << ",";
        oss << ids[i];
    }
    if (ids.size() > limit)
        oss << ",...";
    return oss.str();
}

class tracker_state
{
public:
    void log_tx(const std::string& message)
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        int frame_id = 0;
        const bool parsed = parse_frame_id(message, &frame_id);
        if (parsed && m_have_last_tx && frame_id <= m_last_tx_id)
        {
            reset_unlocked();
            std::cout << "[frame_id_tracker reset] reason=tx_id_restarted id=" << frame_id << std::endl;
        }

        ++m_tx_total;
        if (parsed)
        {
            m_have_last_tx = true;
            m_last_tx_id = frame_id;
            m_pending.emplace(frame_id, message);
            std::cout << "[frame_id_tracker tx] id=" << frame_id
                      << " tx=" << m_tx_total
                      << " rx_ok=" << m_rx_ok_total
                      << " rx_bad=" << m_rx_bad_total
                      << " lost=" << m_lost_total
                      << " pending=" << m_pending.size()
                      << " msg=\"" << message << "\""
                      << std::endl;
        }
        else
        {
            ++m_tx_unparsed_total;
            std::cout << "[frame_id_tracker tx] id=?"
                      << " tx=" << m_tx_total
                      << " rx_ok=" << m_rx_ok_total
                      << " rx_bad=" << m_rx_bad_total
                      << " lost=" << m_lost_total
                      << " pending=" << m_pending.size()
                      << " msg=\"" << message << "\""
                      << std::endl;
        }
    }

    void log_rx(const std::string& message, bool crc_valid)
    {
        std::lock_guard<std::mutex> lock(m_mutex);

        int frame_id = 0;
        const bool parsed = parse_frame_id(message, &frame_id);
        if (crc_valid)
            ++m_rx_ok_total;
        else
            ++m_rx_bad_total;

        if (!parsed)
        {
            ++m_rx_unparsed_total;
            std::cout << "[frame_id_tracker rx] id=?"
                      << " status=" << (crc_valid ? "ok" : "bad")
                      << " tx=" << m_tx_total
                      << " rx_ok=" << m_rx_ok_total
                      << " rx_bad=" << m_rx_bad_total
                      << " lost=" << m_lost_total
                      << " pending=" << m_pending.size()
                      << " msg=\"" << message << "\""
                      << std::endl;
            return;
        }

        std::vector<int> lost_now;
        for (auto it = m_pending.begin(); it != m_pending.end() && it->first < frame_id;)
        {
            lost_now.push_back(it->first);
            it = m_pending.erase(it);
        }
        m_lost_total += lost_now.size();

        const bool matched = (m_pending.erase(frame_id) != 0);
        std::cout << "[frame_id_tracker rx] id=" << frame_id
                  << " status=" << (crc_valid ? "ok" : "bad")
                  << " matched=" << (matched ? 1 : 0)
                  << " tx=" << m_tx_total
                  << " rx_ok=" << m_rx_ok_total
                  << " rx_bad=" << m_rx_bad_total
                  << " lost=" << m_lost_total
                  << " pending=" << m_pending.size();

        if (!lost_now.empty())
            std::cout << " lost_now=" << summarize_ids(lost_now);

        std::cout << " msg=\"" << message << "\""
                  << std::endl;
    }

private:
    void reset_unlocked()
    {
        m_pending.clear();
        m_tx_total = 0;
        m_tx_unparsed_total = 0;
        m_rx_ok_total = 0;
        m_rx_bad_total = 0;
        m_rx_unparsed_total = 0;
        m_lost_total = 0;
        m_have_last_tx = false;
        m_last_tx_id = -1;
    }

    std::mutex m_mutex;
    std::map<int, std::string> m_pending;
    std::size_t m_tx_total = 0;
    std::size_t m_tx_unparsed_total = 0;
    std::size_t m_rx_ok_total = 0;
    std::size_t m_rx_bad_total = 0;
    std::size_t m_rx_unparsed_total = 0;
    std::size_t m_lost_total = 0;
    bool m_have_last_tx = false;
    int m_last_tx_id = -1;
};

tracker_state& state()
{
    static tracker_state instance;
    return instance;
}

} // namespace

void log_tx(const std::string& message)
{
    state().log_tx(message);
}

void log_rx(const std::string& message, bool crc_valid)
{
    state().log_rx(message, crc_valid);
}

} // namespace frame_id_tracker
} // namespace lora_sdr_fmcw_0
} // namespace gr
