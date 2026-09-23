"""raftkv —— 从零实现的基于 Raft 共识算法的分布式 KV 存储。

模块划分：
    rpc      RPC 层：自定义序列化格式、TCP 传输、进程内模拟网络、故障注入
    kvstore  状态机：内存 KV，支持 TTL / Watch / MULTI-EXEC 事务 / MVCC
    raft     Raft 核心：Leader 选举（含 Pre-Vote）、日志复制、安全性、
             Joint Consensus 成员变更、快照
    server   节点服务器：把 Raft、状态机、传输层组装起来，对外提供客户端协议
    client   客户端：自动路由到 Leader 的 CLI 客户端
"""

__version__ = "0.1.0"
