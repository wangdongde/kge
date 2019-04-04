from kge.job import Job


class EvaluationJob(Job):
    def __init__(self, config, dataset, model):
        super().__init__(config, dataset)

        self.config = config
        self.dataset = dataset
        self.model = model
        self.batch_size = config.get('eval.batch_size')
        self.device = self.config.get('job.device')
        self.max_k = self.config.get('eval.max_k')
        self.config.check('train.trace_level', ['example', 'batch', 'epoch'])
        self.trace_examples = self.config.get('eval.trace_level') == 'example'
        self.trace_batch = self.trace_examples or \
            self.config.get('train.trace_level') == 'batch'
        self.config.check('eval.data', ['valid','test'])
        self.eval_data = config.get('eval.data')
        self.filter_valid_with_test = config.get('valid.filter_with_test')
        self.epoch = -1

    def create(config, dataset, model=None):
        """Factory method to create an evaluation job """
        from kge.job import EntityRankingJob, EntityPairRankingJob

        # create the job
        if config.get('eval.type') == 'entity_ranking':
            return EntityRankingJob(config, dataset, model)
        elif config.get('eval.type') == 'entity_pair_ranking':
            return EntityPairRankingJob(config, dataset, model)
        else:
            raise ValueError("eval.type")

    def run(self) -> dict:
        """ Compute evaluation metrics, output results to trace file """
        raise NotImplementedError

    def resume(self):
        # load model
        from kge.job import TrainingJob
        training_job = TrainingJob.create(self.config, self.dataset)
        training_job.resume()
        self.model = training_job.model
        self.epoch = training_job.epoch