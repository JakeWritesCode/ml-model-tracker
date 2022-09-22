from training_log import ModelTrainingLog

training_log = ModelTrainingLog()
training_log.create_log_file()
training_log.commit()
training_log.check_for_non_log_changes()