#ALTER TABLE `stock`.`stock_labo_nomenclaturelotstat` CHANGE COLUMN `nbr_ligne_roxane` `nbr_ligne_robot` INT(11) NULL DEFAULT NULL ;
#ALTER TABLE `stock_dev`.`stock_labo_nomenclaturelotstat` CHANGE COLUMN `nbr_ligne_roxane` `nbr_ligne_robot` INT(11) NULL DEFAULT NULL ;

ALTER TABLE `stock`.`stock_labo_nomenclaturelotstat` CHANGE COLUMN `responsable_creation` `responsable_creation_login` VARCHAR(30) NULL DEFAULT NULL ;
ALTER TABLE `stock_dev`.`stock_labo_nomenclaturelotstat` CHANGE COLUMN `responsable_creation` `responsable_creation_login` VARCHAR(30) NULL DEFAULT NULL ;
