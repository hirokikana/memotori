/**
 * DEBUG
 */
/*
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `memo`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `category_share`;
DROP TABLE IF EXISTS `friend`;
*/

CREATE TABLE IF NOT EXISTS `user` (
	   `id` int(11) unsigned not null AUTO_INCREMENT,
	   `name` varchar(255),
	   `mail` char(255) not null UNIQUE,
	   `password` varchar(255) not null,
	   `create_date` datetime not null,
	   `update_date` datetime not null,
	   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'ユーザー情報管理テーブル';

CREATE TABLE IF NOT EXISTS `memo` (
	   `id` int(11) unsigned not null AUTO_INCREMENT,
	   `uid` int(11) unsigned not null,
	   `content` text,
	   `create_date` datetime not null,
	   `update_date` datetime not null,
	   PRIMARY KEY (`id`),
	   INDEX `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'メモ情報管理テーブル';

CREATE TABLE IF NOT EXISTS `category` (
	   `id` int(11) unsigned not null auto_increment,
	   `uid` int(11) unsigned not null,
	   `name` varchar(255), 
	   `create_date` datetime not null,
	   `update_date` datetime  not null,
	   PRIMARY KEY (`id`),
	   INDEX `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'カテゴリ保存テーブル';

CREATE TABLE IF NOT EXISTS `category_share` (
	   `id` int(11) unsigned not null auto_increment,
	   `uid` int(11) unsigned not null,
	   `cid` int(11) unsigned not null,
	   PRIMARY KEY (`id`),
	   INDEX `uid` (`uid`),
	   INDEX `cid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'カテゴリ共有情報テーブル';

CREATE TABLE IF NOT EXISTS `friend` (
	   `id` int(11) unsigned not null auto_increment,
	   `src_uid` int(11) unsigned not null,
	   `dst_uid` int(11) unsigned not null,
	   PRIMARY KEY (`id`),
	   INDEX `src_uid` (`src_uid`),
	   INDEX `dst_uid` (`dst_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '友達情報管理テーブル';


