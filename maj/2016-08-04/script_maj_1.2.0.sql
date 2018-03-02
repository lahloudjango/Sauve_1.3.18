REPAIR TABLE `stock`.`auth_group` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`auth_group_permissions` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`auth_permission` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`auth_user` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`auth_user_groups` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`auth_user_user_permissions` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`django_admin_log` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`django_content_type` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`django_migrations` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`django_session` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`django_site` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_contenant` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_contenantstat` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_contenanttype` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_droits_fonctions` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_impression` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_impressiondetail` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_impressionimprimante` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_impressionimprimanteparam` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_impressionimprimanteparamdetail` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_log` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_nomenclaturelot` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_nomenclaturelotingredient` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_nomenclaturelotingredientdosage` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_nomenclaturelotstat` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_nomenclaturetype` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_siteentrepotmagasin` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_stockentrepot` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_stockmagasin` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_stocksite` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_unitmasse` EXTENDED USE_FRM;
REPAIR TABLE `stock`.`stock_labo_userpreference` EXTENDED USE_FRM;


ALTER TABLE `stock`.`stock_labo_nomenclature` DROP COLUMN `commentaire_ancien`;
ALTER TABLE `stock`.`stock_labo_nomenclature` DROP COLUMN `description_ancien`;
ALTER TABLE `stock`.`stock_labo_nomenclature` DROP COLUMN `code_ancien`;
ALTER TABLE `stock`.`stock_labo_nomenclature` ADD COLUMN `collection` TINYINT(1) NOT NULL  AFTER `duree_validite`;

ALTER TABLE `stock`.`stock_labo_contenantstat` CHANGE COLUMN `contenant_provemance_site_code` `contenant_provenance_site_code` VARCHAR(30) DEFAULT NULL;
ALTER TABLE `stock`.`stock_labo_contenantstat` CHANGE COLUMN `contenant_provemance_site_description` `contenant_provenance_site_description` VARCHAR(100) DEFAULT NULL;

ALTER TABLE `stock`.`stock_labo_contenantstat` CHANGE COLUMN `nomenclature_lot_client` `nomenclature_lot_client` VARCHAR(50) DEFAULT NULL;
ALTER TABLE `stock`.`stock_labo_contenantstat` CHANGE COLUMN `nomenclature_lot_projet` `nomenclature_lot_projet` VARCHAR(50) DEFAULT NULL;

ALTER TABLE `stock`.`stock_labo_nomenclaturelot` ADD COLUMN `nbr_ligne_roxane` INT(11) DEFAULT NULL AFTER `num_roxane`;
ALTER TABLE `stock`.`stock_labo_nomenclaturelot` ADD COLUMN `nbr_ligne_manuel` INT(11) DEFAULT NULL AFTER `nbr_ligne_roxane` ;

CREATE TABLE `stock_labo_nomenclaturelotstat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(30) DEFAULT NULL,
  `nomenclature_code` varchar(30) DEFAULT NULL,
  `nomenclature_description` varchar(100) DEFAULT NULL,
  `date_creation` date DEFAULT NULL,
  `client` varchar(50) DEFAULT NULL,
  `client_ka` varchar(50) DEFAULT NULL,
  `projet` varchar(50) DEFAULT NULL,
  `poids_reference` double DEFAULT NULL,
  `num_roxane` varchar(12) DEFAULT NULL,
  `nbr_ligne_roxane` int(11) DEFAULT NULL,
  `nbr_ligne_manuel` int(11) DEFAULT NULL,
  `responsable_creation` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



#ALTER TABLE `stock`.`auth_group` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`auth_group_permissions` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`auth_permission` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`auth_user` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`auth_user_groups` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`auth_user_user_permissions` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`django_admin_log` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`django_content_type` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`django_migrations` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`django_session` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`django_site` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_contenant` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_contenantstat` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_contenanttype` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_droits_fonctions` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_impression` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_impressiondetail` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_impressionimprimante` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_impressionimprimanteparam` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_impressionimprimanteparamdetail` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_log` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclature` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclaturelot` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclaturelotingredient` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclaturelotingredientdosage` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclaturelotstat` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_nomenclaturetype` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_siteentrepotmagasin` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_stockentrepot` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_stockmagasin` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_stocksite` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_unitmasse` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;
#ALTER TABLE `stock`.`stock_labo_userpreference` CHARACTER SET = utf8 , COLLATE = utf8_unicode_ci ;

UPDATE stock.django_admin_log set change_message = "mouvement déplacement" WHERE change_message = "mouvement deplassement";
ALTER TABLE `stock`.`stock_labo_contenant` CHANGE COLUMN `provemance_site_id` `provenance_site_id` INT(11) NOT NULL  ;
ALTER TABLE `stock`.`stock_labo_nomenclaturelot` ADD COLUMN `client_ka` VARCHAR(50) NULL DEFAULT ''  AFTER `client` ;

