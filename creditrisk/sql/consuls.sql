CREATE OR REPLACE FUNCTION insertprediction()
  RETURNS trigger AS
$BODY$
BEGIN
	insert into prediction(idvalidacion, dateevaluation, dt_class0, dt_class1, rnn_class0, rnn_class1, svm_class0, svm_class1, 
						  	rl_class0, rl_class1, xgboost_class0, xgboost_class1)
	values (new.id_evaluation, NOW(), 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00);
    RETURN NEW;
END;
$BODY$
language plpgsql;

CREATE TRIGGER trigger_prediction
after insert
ON evaluation
FOR EACH ROW
EXECUTE PROCEDURE insertprediction();

select * from prediction;

INSERT INTO evaluation (edad, codigopostal, tipovivienda, dependientes, estadocivil, genero, ocupacion, nivelacademico, telefono, ingreso, egreso, tipoprestamo, 
						tasanormal, tasamoratoria, monto, avales, creditostrabajados, bien, montogarantia, finalidad, remesas, plazo, evaluador, nombrecompleto, domicilio) 
VALUES (30, 70720, 2, 0, 2, 1,0191023,2,1,12000.50,4000.20,12,48,48,50000.50,2,2,5,25000.50,1,1,12,1,'Karina Pascual Fabian', 'Colonia Cuahtemoc, Matias Romero');