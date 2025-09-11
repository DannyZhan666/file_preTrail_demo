# 数据库初始化

-- 创建库
create database if not exists file_task;

-- 切换库
use file_task;

-- 用户表
DROP TABLE IF EXISTS file_task.`user`;
create table if not exists file_task.`user`
(
    username      varchar(256)                       null comment '用户昵称',
    id            bigint auto_increment comment '主键'
        primary key,
    user_account  varchar(256)                       null comment '账号',
    user_password varchar(512)                       not null comment '密码',
    gender        tinyint                            null comment '性别',
    avatar_url    varchar(1024)                      null comment '用户头像',
    phone         varchar(128)                       null comment '手机号',
    email         varchar(512)                       null comment '邮箱',
    user_status   int      default 0                 not null comment '状态',
    user_role     int      default 1                 not null comment '用户角色 0-管理员 1-律师 2-客户',
    create_time   datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    update_time   datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    is_deleted    tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
)
    comment '用户表';


-- 文件表
DROP TABLE IF EXISTS file_task.`file`;
create table if not exists file_task.`file`
(
    `id`          bigint                             not null auto_increment comment '文件id' primary key,
    `file_name`   varchar(256)                       not null comment '文件名',
    `file_type`   VARCHAR(50)                        not null comment '文件类型',
    `path`        varchar(1024)                      not null comment '文件路径',
    `content`     LONGBLOB                           not null comment '文件内容',
    `create_time` datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    `update_time` datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`  tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '文件表';


-- 工单表
DROP TABLE IF EXISTS file_task.`job`;
create table if not exists file_task.`job`
(
    `id`             bigint                             not null auto_increment comment '工单id' primary key,
    `job_name`       varchar(256)                       not null comment '工单名',
    `job_type`       int                                not null comment '工单种类',
    `job_intro`      varchar(1024) comment '工单简介',
    `file_id`        bigint                             not null comment '文件id',
    `client_id`      bigint                             not null comment '客户id',
    `client_budget`  bigint                             null comment '客户预算',
    `due`            datetime                           null comment '预期时间',
    `lawyer_id`      bigint                             null comment '律师id',
    `lawyer_budget`  bigint                             null comment '律师预算',
    `lawyer_comment` varchar(2048)                      null comment '律师批注',
    `due_law`        datetime                           null comment '律师的预期时间',
    `job_status`     tinyint  default 0                 not null comment '工单状态 0-未被接 1-已改动 2-已完成',
    `create_time`    datetime                           not null comment '创建时间',
    `update_time`    datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`     tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '工单表';

-- -----------------------------------------------------------

-- 新工单表
DROP TABLE IF EXISTS file_task.`newJob`;
create table if not exists file_task.`newJob`
(
    `id`             bigint                             not null auto_increment comment '工单id' primary key,
    `job_id`         bigint                             null comment '原工单id',
    `job_name`       varchar(256)                       not null comment '工单名',
    `job_type`       int                                not null comment '工单种类',
    `job_intro`      varchar(1024) comment '工单简介',
    `file_id`        bigint                             not null comment '文件id',
    `client_id`      bigint                             not null comment '客户id',
    `client_budget`  bigint                             null comment '客户预算',
    `due`            datetime                           null comment '逾期时间',
    `lawyer_id`      bigint                             null comment '律师id',
    `lawyer_budget`  bigint                             null comment '律师预算',
    `lawyer_comment` varchar(2048)                      null comment '律师批注',
    `due_law`        datetime                           null comment '律师的预期时间',
    `job_status`     tinyint  default 0                 not null comment '工单状态 0-未被接 1-已改动 2-已完成',
    `create_time`    datetime                           not null comment '创建时间',
    `update_time`    datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`     tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '新工单表';

-- 投标表
DROP TABLE IF EXISTS file_task.`bids`;
create table if not exists file_task.`bids`
(
    `id`             bigint                             not null auto_increment comment '投标id' primary key,
    `jid`            bigint                             not null comment '工单id',
    `lawyer_id`      bigint                             null comment '律师id',
    `lawyer_budget`  bigint                             null comment '律师预算',
    `lawyer_comment` varchar(2048)                      null comment '律师批注',
    `create_time`    datetime                           not null comment '创建时间',
    `update_time`    datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`     tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '投标表';

-- ------------------------------------------------------------

-- 订单表
DROP TABLE IF EXISTS file_task.`orders`;
create table if not exists file_task.`orders`
(
    `id`          bigint                             not null auto_increment comment '订单id' primary key,
    `order_name`  varchar(256)                       not null comment '订单名',
    `client_id`   bigint                             not null comment '客户id',
    `lawyer_id`   bigint                             not null comment '律师id',
    `new_jid`     bigint                             not null comment '新工单id',
    `origin_jid`  bigint                             not null comment '原工单id',
    `create_time` datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    `update_time` datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`  tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '订单表';


-- 预审结果表
DROP TABLE IF EXISTS file_task.`file_review_results`;
create table if not exists file_task.`file_review_results`
(
    `id`          bigint                             not null auto_increment comment '主键' primary key,
    `uid`         bigint                             not null comment '用户id',
    `fid`         bigint                             not null comment '文件id',
    `create_time` datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    `update_time` datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`  tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '预审结果表';


-- 文件内容分段表
DROP TABLE IF EXISTS file_task.`file_seg_results`;
create table if not exists file_task.`file_seg_results`
(
    `id`          bigint                             not null auto_increment comment '段落id' primary key,
    `fid`         bigint                             not null comment '文件id',
    paragraph             longtext                   null comment '原段落',
    page_num              int                        null comment 'page_num',
    paragraph_clean       text                       null comment 'paragraph_clean',
    model_predict_details longtext                   null comment 'model_predict_details',
    model_predict_labels  longtext                   null comment 'model_predict_labels',
    `create_time` datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    `update_time` datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    `is_deleted`  tinyint  default 0                 not null comment '是否删除(0-未删, 1-已删)'
) comment '文件内容分段表';


