from collections.abc import Generator
import csv
import requests
import time
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

type MessageList = list[dict[str, Any]]


def fetch_messages_batch(
    channel_id: str, s: requests.Session, before: str | None = None
) -> MessageList:
    """Fetch a single batch of messages (up to 100)"""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    params = {"limit": 100}

    if before:
        params["before"] = before

    while True:
        response = s.get(url, params=params)

        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            continue

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return []

        return response.json()


def fetch_all_messages(channel_id: str, s: requests.Session) -> MessageList:
    """Fetch all messages from a Discord channel"""
    all_messages: MessageList = []
    before: str | None = None

    print(f"Fetching messages from channel {channel_id}...")

    while True:
        batch = fetch_messages_batch(channel_id, s, before)

        if not batch:
            break

        all_messages.extend(batch)
        print(f"Fetched {len(batch)} messages (total: {len(all_messages)})")

        # If we got less than 100, we're done
        if len(batch) < 100:
            break

        # Use the oldest message ID for next batch
        before = batch[-1]["id"]

        # Be nice to Discord's API
        time.sleep(5)

    return all_messages


def get_dates(messages: MessageList) -> Generator[tuple[int, str]]:
    count = 0
    for msg in messages:
        if not msg["author"]["username"].startswith("Carl-bot") or not msg["embeds"]:
            continue

        e = msg["embeds"][0]
        # Parse the date
        date = msg["timestamp"].split(".", 1)[0].replace("T", " ")

        if e["title"] == "Member joined":
            # Remove user id
            count = e["description"].split("> ", 1)[-1]
            # Remove segment after the total member count
            index = count.index(" ") - 2
            count = int(count[:index])
            yield (count, date)
        elif e["title"] == "Member left" and count:
            count -= 1
            yield (count, date)


def create_graph():
    plt.rcParams["toolbar"] = "none"

    file = pd.read_csv("counts.csv")
    file = file.iloc[::-1].reset_index(drop=True)
    dates = pd.to_datetime(file["date"], format="ISO8601", utc=True)
    member_counts = file["count"]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.canvas.manager.set_window_title("Kiwi Nest 2025 Member Growth")

    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_yticks([])

    ax.set_xlim(pd.Timestamp(f'{min(dates).year}-01-01', tz='UTC'), max(dates))
    ax.set_ylim(0, max(member_counts) * 1.1)
    ax.set_aspect("auto")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    plt.setp(
        ax.get_xticklabels(), color="#524A9B", font="Gloria Hallelujah", fontsize=8
    )

    (line,) = ax.plot([], [], color="#524A9B", lw=0.696969696969)

    top_text = ax.text(
        0.5,
        0.995,
        "",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=12,
        fontweight="bold",
        color="#524A9B",
        font="Gloria Hallelujah",
    )
    member_text = ax.text(
        0.5,
        0.03,
        "",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#524A9B",
        font="Gloria Hallelujah",
    )

    def update(frame):
        line.set_data(dates[:frame], member_counts[:frame])
        top_text.set_text("KiwiNest 2025 Membercount")
        member_text.set_text(f"Members: {member_counts[frame-1]:,.0f}")
        return line, top_text, member_text

    ani = FuncAnimation(
        fig,
        update,
        frames=range(1, len(dates) + 1),
        interval=1,
        blit=False,
        repeat=False,
    )

    # If you would like to save it locally,
    # uncomment the two lines, and comment the plt.show()

    # ani.save('membercount.mp4', writer='ffmpeg', fps=120)
    # print("Video Saved!")

    plt.show()


def main(CHANNEL_ID: str) -> None:
    """Main execution"""
    with open("TOKEN", "rt") as f:
        BOT_TOKEN = f.read().strip()

    s = requests.Session()
    s.headers.update(
        {
            "Authorization": f"Bot {BOT_TOKEN}",
            "User-Agent": "MemberCount (requests, 2.9)",
        }
    )

    messages = fetch_all_messages(CHANNEL_ID, s)

    print(f"Completed! Fetched {len(messages)} total messages")

    with open("counts.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(["count", "date"])

        # Write data rows
        writer.writerows(get_dates(messages))

    create_graph()


if __name__ == "__main__":
    main("1328638584575492137")
