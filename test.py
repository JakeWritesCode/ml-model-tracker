from training_log import ModelTrainingLog

training_log = ModelTrainingLog()
training_log.create_log_file()
training_log.commit()
training_log.train_results = {"a": "result"}
training_log.training_params = {"a": 1}
training_log.test_results = {"Result": "Very good"}
training_log.log()