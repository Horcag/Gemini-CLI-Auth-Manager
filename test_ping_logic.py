import sys
from datetime import datetime, timezone

def test_logic():
    # User's exact reset times
    reset_times = {
        "arthur.bennett.924@gmail.com": "2026-05-12T09:40:55Z",
        "clawawinston220@gmail.com": "2026-05-12T15:05:46Z",
        "hariharsahani1990@gmail.com": "2026-05-13T01:39:26Z",
        "jackdinloa@gmail.com": "2026-05-13T09:05:02Z",
        "nikita20805.dev@gmail.com": "2026-05-12T13:37:10Z",
        "nikita20805@gmail.com": "2026-05-13T09:05:06Z",
        "rachet337@gmail.com": "2026-05-12T14:40:21Z",
        "weberthomas529@gmail.com": "2026-05-13T02:07:42Z"
    }

    # The time when the user ran the command was approx 13:04:48 local time
    # From the reset times, it appears local time is UTC+4.
    # So 13:04:48 UTC+4 is 09:04:48 UTC. Let's use exactly 09:04:48 UTC on May 12, 2026.
    now_utc = datetime(2026, 5, 12, 9, 4, 48, tzinfo=timezone.utc)

    print(f"Simulated Current Time (UTC): {now_utc}")
    print("-" * 50)

    for email, reset_time_str in reset_times.items():
        rt = datetime.fromisoformat(reset_time_str.replace("Z", "+00:00"))
        
        diff = rt - now_utc
        time_diff_hours = diff.total_seconds() / 3600.0
        
        needs_ping = False
        if time_diff_hours >= 23.95:
            needs_ping = True

        status = "Dormant (Needs Ping)" if needs_ping else "Active"
        
        hours = int(time_diff_hours)
        mins = int((time_diff_hours * 60) % 60)
        
        print(f"{email}:")
        print(f"  Reset Time: {reset_time_str}")
        print(f"  Time Diff: {time_diff_hours:.2f} hours ({hours}h {mins}m)")
        print(f"  Needs Ping: {needs_ping}")
        print("-" * 20)

if __name__ == '__main__':
    test_logic()
