"""raftkv - 从零实现的基于 Raft 共识算法的分布式 KV 存储。

模块划分:
    storage       持久化(hard state / 日志 / 快照)
    statemachine  MVCC 内存 KV 状态机(TTL / CAS / 事务 / Watch)
    network       传输层(TCP 传输 + 可注入故障的模拟网络)
    raft          Raft 共识核心(选举 / 复制 / 安全 / 快照 / 成员变更)
    server        节点服务(对外客户端协议 + 优雅上下线)
    client        客户端库与 CLI(自动路由到 Leader)
"""

__version__ = "1.0.0"
