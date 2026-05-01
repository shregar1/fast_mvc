# 📡 FastChannels

**WebSocket channel abstraction with pub/sub rooms and presence tracking.**

FastChannels provides a clean, framework-aligned abstraction over WebSocket connections — supporting named rooms, pub/sub messaging, presence awareness, and pluggable backends (in-memory or Redis).

---

## 🏗️ Core Features

| Feature | Description |
|---------|-------------|
| **Channel Rooms** | Named pub/sub rooms with automatic lifecycle management. |
| **Presence Tracking** | Know which users are connected to which rooms in real-time. |
| **Redis Backend** | Scale beyond a single process with Redis pub/sub. |
| **In-Memory Backend** | Zero-config default for development and single-process deployments. |
| **Broadcast & Whisper** | Send to all room members or target specific connections. |
| **Middleware Integration** | Plugs into the FastX middleware pipeline for auth-aware channels. |

---

## ⚡ Quick Example

```python
from fastx_channels import ChannelLayer, Room

layer = ChannelLayer()

# Join a room
await layer.join("chat:general", connection_id="user-123")

# Broadcast to all members
await layer.broadcast("chat:general", {"type": "message", "text": "Hello!"})

# Check presence
members = await layer.presence("chat:general")
```

---

## 🔌 Redis Backend (Multi-Process)

```python
from fastx_channels.backends.redis import RedisChannelBackend

layer = ChannelLayer(backend=RedisChannelBackend(redis_url="redis://localhost:6379"))
```

---

## 🛠️ Installation

```bash
pip install fastx-channels           # In-memory only
pip install fastx-channels[redis]    # With Redis backend
```

---

## 🔗 Related

- **Ecosystem overview** — full map of packages.
- **WebSocket Channels** — framework-level WebSocket patterns.
- **Server-Sent Events** — one-way push alternative.
