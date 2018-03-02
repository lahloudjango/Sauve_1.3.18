#ALTER TABLE `stock_dev`.`stock_labo_contenant` DROP COLUMN `responsable_suppression_login`;

#ALTER TABLE `stock_dev`.`stock_labo_contenant` ADD COLUMN `responsable_creation_id` INT(11) NULL DEFAULT NULL AFTER `responsable_mouvement_id`;

#ALTER TABLE `stock_dev`.`stock_labo_contenantstat` ADD COLUMN `contenant_responsable_creation_login` VARCHAR(30) NULL DEFAULT NULL AFTER `contenant_date_creation`;

#ALTER TABLE `stock_dev`.`stock_labo_nomenclaturelotstat` ADD COLUMN `nomenclature_type_code` VARCHAR(30) NULL DEFAULT NULL AFTER `nomenclature_description`;

#UPDATE `stock_dev`.`stock_labo_nomenclaturelot` SET `responsable_creation_id`=74 WHERE `responsable_creation_id` is null AND `date_creation` > "2017-01-15";

#TRUNCATE `stock_dev`.`stock_labo_nomenclaturelotstat`

