from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact",
                                    ['train_file_path','test_filepath','is_ingested','message'])
                                    