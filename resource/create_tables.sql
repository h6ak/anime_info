DROP TABLE IF EXISTS `stations`;
CREATE TABLE `stations` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='放送局';

DROP TABLE IF EXISTS `animations`;
CREATE TABLE `animations` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `official_site` varchar(255) DEFAULT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='アニメ';

DROP TABLE IF EXISTS `first_onair_infomations`;
CREATE TABLE `first_onair_infomations` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `animation_id` bigint(20) unsigned NOT NULL,
    `station_id` int(10) unsigned NOT NULL,
    `start_at` date DEFAULT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`animation_id`) REFERENCES `animations` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`station_id`) REFERENCES `stations` (`id`) ON DELETE CASCADE,
    UNIQUE KEY (`animation_id`, `station_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='アニメ放送開始情報';
