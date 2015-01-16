

1)openstack 多控制节点pacemaker集群配置向导实践文档
安装环境CENTOS6U5_X64 CENTOS6U6_X64 
 pacemaker_config.txt 
 
2) pacemaker 使用zabbix监控脚本，正常情况返回为0，节点无集群状态返回-1，存在offline 节点或存在资源resources stop等异常状态返回大于1，为异常服务数量
   pacemaker_status.py
