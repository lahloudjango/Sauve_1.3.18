
USE `stock_dev`;

ALTER TABLE `stock_labo_nomenclaturelot` ADD COLUMN `commentaire` longtext NOT NULL AFTER `definition` ;
ALTER TABLE `stock_labo_nomenclaturelot` ADD COLUMN `client` varchar(50) NOT NULL AFTER `commentaire` ;
ALTER TABLE `stock_labo_nomenclaturelot` ADD COLUMN `projet` varchar(50) NOT NULL AFTER `client` ;
ALTER TABLE `stock_labo_nomenclaturelot` ADD COLUMN `poids_reference` DOUBLE NULL  AFTER `projet` ;

DELETE FROM `stock_labo_nomenclaturelotinfo` WHERE `id`='586';
DELETE FROM `stock_labo_nomenclaturelotinfo` WHERE `id`='1066';
DELETE FROM `stock_labo_nomenclaturelotinfo` WHERE `id`='1263';

UPDATE `stock_labo_nomenclaturelot`, `stock_labo_nomenclaturelotinfo`
	SET `stock_labo_nomenclaturelot`.`commentaire` = `stock_labo_nomenclaturelotinfo`.`commentaire`,
		`stock_labo_nomenclaturelot`.`client` = `stock_labo_nomenclaturelotinfo`.`client`,
		`stock_labo_nomenclaturelot`.`projet` = `stock_labo_nomenclaturelotinfo`.`projet`
	WHERE `stock_labo_nomenclaturelot`.`id` = `stock_labo_nomenclaturelotinfo`.`nomenclature_lot_id`
		AND `stock_labo_nomenclaturelotinfo`.`projet` != "";

UPDATE `stock_labo_nomenclature`, `stock_labo_nomenclaturelot`
	SET `stock_labo_nomenclaturelot`.`poids_reference` = `stock_labo_nomenclature`.`poids_reference`
	WHERE `stock_labo_nomenclature`.`id` = `stock_labo_nomenclaturelot`.`nomenclature_id`;

#UPDATE `stock`.`stock_labo_nomenclature` AS `new`, `stock_old`.`stock_labo_nomenclature` AS `old`
#	SET `new`.`code_ancien` = `old`.`code`
#	WHERE `new`.`id` = `old`.`id`;
UPDATE `stock`.`stock_labo_nomenclature`
	SET `stock_labo_nomenclature`.`code_ancien` = `stock_labo_nomenclature`.`code`;

ALTER TABLE `stock_labo_contenant` ADD COLUMN `responsable_suppression_login` VARCHAR(30) NULL AFTER `provemance_site_id`;
ALTER TABLE `stock_labo_contenant` ADD COLUMN `responsable_suppression_id` INT(11) NULL AFTER `responsable_suppression_login`;
ALTER TABLE `stock_labo_contenant` ADD INDEX `stock_labo_contenant_00000001` (`responsable_suppression_id` ASC) ;
ALTER TABLE `stock_labo_contenant` ADD COLUMN `responsable_mouvement_id` INT(11) NULL  AFTER `responsable_suppression_id` ;
ALTER TABLE `stock_labo_contenant` ADD INDEX `stock_labo_contenant_00000002` (`responsable_mouvement_id` ASC) ;

#ALTER TABLE `stock_labo_contenant` ADD UNIQUE KEY `stock_labo_contenant` (`responsable_suppression_id`) ;
#ALTER TABLE `stock_labo_contenant` ADD UNIQUE KEY `stock_labo_contenant` (`responsable_mouvement_id`) ;
#ALTER TABLE `stock_labo_contenant` ADD INDEX `stock_labo_contenant_145179f4` (`responsable_suppression_id` ASC) ;
#ALTER TABLE `stock_labo_contenant` DROP INDEX `stock_labo_contenant_dc5b5d5c` ;
#ALTER TABLE `stock_labo_contenant` ADD UNIQUE KEY `stock_labo_contenant` (`panie_user_id`) ;
#ALTER TABLE `stock_labo_contenant` ADD INDEX `stock_labo_contenant_00000001` (`panier_user_id` ASC) ;

CREATE TABLE `stock_labo_contenantstat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenant_type_code` varchar(30) DEFAULT NULL,
  `contenant_code` varchar(30) DEFAULT NULL,
  `contenant_date_creation` date DEFAULT NULL,
  `contenant_provemance_site_code` varchar(30) DEFAULT NULL,
  `contenant_provemance_site_description` varchar(100) DEFAULT NULL,
  `contenant_date_suppression` date DEFAULT NULL,
  `contenant_responsable_suppression_login` varchar(30) DEFAULT NULL,
  `nomenclature_lot_code` varchar(30) DEFAULT NULL,
  `nomenclature_lot_client` varchar(30) DEFAULT NULL,
  `nomenclature_lot_projet` varchar(100) DEFAULT NULL,
  `nomenclature_lot_poids_reference` double DEFAULT NULL,
  `nomenclature_code` varchar(30) DEFAULT NULL,
  `nomenclature_description` varchar(100) DEFAULT NULL,
  `nomenclature_type_code` varchar(30) DEFAULT NULL,
  `nomenclature_type_description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

ALTER TABLE `stock_labo_nomenclature` ADD COLUMN `code_ancien` VARCHAR(30) NULL DEFAULT NULL  AFTER `code`;
UPDATE stock_dev.stock_labo_nomenclature SET stock_labo_nomenclature.code_ancien = stock_labo_nomenclature.code;

CREATE TABLE `stock_labo_impressionimprimanteparam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `stock_labo_impressionimprimanteparamdetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(100) NOT NULL,
  `impression_imprimante_param_id` int(11) NOT NULL,
  `champ_data` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stock_labo_impressionimprimanteparamdetail_388a3cdb` (`impression_imprimante_param_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

ALTER TABLE `stock_labo_impressionimprimante` ADD COLUMN `param_pre_impression_id` INT(11) NULL DEFAULT NULL  AFTER `imprimante_port`;
ALTER TABLE `stock_labo_impressionimprimante` ADD COLUMN `param_post_impression_id` INT(11) NULL DEFAULT NULL  AFTER `param_pre_impression_id` ;




ALTER TABLE `stock_labo_nomenclature` DROP COLUMN `poids_reference` ;
DROP TABLE `stock_labo_nomenclaturelotinfo`;
